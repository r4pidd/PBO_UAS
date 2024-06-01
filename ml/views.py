import json
import logging
import pandas as pd

from django.shortcuts import render
from datetime import datetime
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from pbo_uas.response import error_with_msg, ok_with_data
from joblib import load


# Load the model and encoders
model = load('ml/machine/RandomForestRegression.joblib')
le = load('ml/machine/le_encoders.pkl')
umur_scaler = load('ml/machine/umur_scaler.pkl')
kuantitas_scaler = load('ml/machine/kuantitas_scaler.pkl')


# @csrf_exempt
@api_view(['POST'])
def pred_qty(request):
    try:
        data = json.loads(request.body)

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

    def transform_label(column, value):
        if value in le[column].classes_:
            return le[column].transform([value])[0]
        else:
            return -1  # or len(le[column].classes_) for a new unique label

    for column in ['Hari', 'Nama', 'Kode', 'Unit', 'Metode Pembayaran']:
        df[column] = df[column].apply(lambda x: transform_label(column, x))

    df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    df['Tanggal'] = (df['Tanggal'] - df['Tanggal'].min()).dt.days

    df['Umur'] = umur_scaler.transform(df['Umur'].values.reshape(-1, 1))

    rf_loaded_pred_scaled = model.predict(df)
    rf_loaded_pred = kuantitas_scaler.inverse_transform(rf_loaded_pred_scaled.reshape(-1,1))
    return int(round(rf_loaded_pred[0][0],0))
