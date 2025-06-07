import os
import pandas as pd
from datetime import datetime


def corregir_fecha(fecha: str) -> str:
    partes = fecha.split('/')
    if len(partes[0]) == 4:
        return '/'.join(reversed(partes))
    return '/'.join(partes)


def normalizar_columnas_texto(df: pd.DataFrame) -> pd.DataFrame:
    df['sexo'] = df['sexo'].str.lower()
    df['tipo_de_emprendimiento'] = df['tipo_de_emprendimiento'].str.lower()
    df['idea_negocio'] = df['idea_negocio'].str.lower().replace({'_': ' ', '-': ' '}, regex=True)
    df['barrio'] = df['barrio'].str.lower().replace({'_': ' ', '-': ' '}, regex=True)
    df['línea_credito'] = df['línea_credito'].str.lower().replace({'_': ' ', '-': ' '}, regex=True)
    return df


def limpiar_monto_credito(df: pd.DataFrame) -> pd.DataFrame:
    df['monto_del_credito'] = df['monto_del_credito'].str.replace(' ', '', regex=False)
    df['monto_del_credito'] = df['monto_del_credito'].str.replace('$', '', regex=False)
    df['monto_del_credito'] = df['monto_del_credito'].str.replace(',', '', regex=False)
    df['monto_del_credito'] = df['monto_del_credito'].astype(float)
    return df


def aplicar_correccion_fecha(df: pd.DataFrame) -> pd.DataFrame:
    df['fecha_de_beneficio'] = df['fecha_de_beneficio'].apply(corregir_fecha)
    return df


def eliminar_duplicados(df: pd.DataFrame) -> pd.DataFrame:
    columnas_clave = [
        "sexo", "tipo_de_emprendimiento", "idea_negocio", "barrio", "estrato",
        "comuna_ciudadano", "fecha_de_beneficio", "monto_del_credito", "línea_credito"
    ]
    return df.drop_duplicates(subset=columnas_clave).dropna()


def pregunta_01():
    df = pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";")
    df = df.dropna()
    df = normalizar_columnas_texto(df)
    df = aplicar_correccion_fecha(df)
    df = limpiar_monto_credito(df)
    df = eliminar_duplicados(df)

    os.makedirs("files/output", exist_ok=True)
    df.to_csv("files/output/solicitudes_de_credito.csv", sep=";", index=False)


pregunta_01()