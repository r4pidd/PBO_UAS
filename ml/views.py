import json
import logging
import os
import pandas as pd

from django.shortcuts import render
from datetime import datetime
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from pbo_uas.response import error_with_msg, ok_with_data
from joblib import load


# Load the model and encoders
current_dir = os.path.dirname(os.path.realpath(__file__))
model_path = os.path.join(current_dir, 'machine/XGBRegression.joblib')
le_path = os.path.join(current_dir, 'machine/le_encoders.pkl')
umur_scaler_path = os.path.join(current_dir, 'machine/umur_scaler.pkl')
kuantitas_scaler_path = os.path.join(current_dir, 'machine/kuantitas_scaler.pkl')

# Load the model and scalers
model = load(model_path)
le = load(le_path)
umur_scaler = load(umur_scaler_path)
kuantitas_scaler = load(kuantitas_scaler_path)


# @csrf_exempt
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def pred_qty(request):
    try:
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)

        name = data.get('name')
        date = data.get('date')
        age = data.get('age')
        product_code = data.get('product_code')
        payment_method = data.get('payment_method')
        unit = 'pcs'

        date_object = datetime.strptime(date, "%Y-%m-%d")
        formatted_date = date_object.strftime("%m/%d/%Y").lstrip("0").replace("/0", "/")

        date_object = datetime.strptime(formatted_date, "%m/%d/%Y")
        day = date_object.strftime("%A")

        pred_qty = predict(name, age, product_code, payment_method, day, date, unit)
        return ok_with_data(pred_qty, 'ok')


    except json.JSONDecodeError:
        return error_with_msg('failed to get body request')

def predict(nama: str, umur: float, kode: str, metode_pembayaran: str, hari: str, tanggal: str, unit: str):
    data = {
        'Umur': [umur],
        'Tanggal': [tanggal],
        'Hari': [hari],
        'Nama': [nama],
        'Kode': [kode],
        'Unit': [unit],
        'Metode Pembayaran': [metode_pembayaran],
    }

    df = pd.DataFrame(data)

    unseen_label = [False]

    def transform_label(column, value):
        if value in le[column].classes_:
            return le[column].transform([value])[0]
        else:
            unseen_label[0] = True
            return -1

    for column in ['Hari', 'Nama', 'Kode', 'Unit', 'Metode Pembayaran']:
        df[column] = df[column].apply(lambda x: transform_label(column, x))

    if unseen_label[0]:
        return 1


    df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    df['Tanggal'] = (df['Tanggal'] - df['Tanggal'].min()).dt.days

    df['Umur'] = umur_scaler.transform(df['Umur'].values.reshape(-1, 1))

    rf_loaded_pred_scaled = model.predict(df)
    rf_loaded_pred = kuantitas_scaler.inverse_transform(rf_loaded_pred_scaled.reshape(-1,1))
    return int(round(rf_loaded_pred[0][0],0))
