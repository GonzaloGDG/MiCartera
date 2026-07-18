"""
Solo las rutas Flask, sin la lógica de negocio. 
La lógica de negocio está en services/yahoo_finance.py
"""
from flask import Blueprint, jsonify, request
from services.yahoo_finance import get_cotizacion, get_historico

cotizaciones_bp = Blueprint('cotizaciones', __name__)

@cotizaciones_bp.route('/cotizacion/<ticker>', methods=['GET'])
def cotizacion(ticker):
    resultado = get_cotizacion(ticker)
    status = 200 if resultado['ok'] else 500
    return jsonify(resultado), status

@cotizaciones_bp.route('/historico/<ticker>', methods=['GET'])
def historico(ticker):
    periodo   = request.args.get('periodo', '1mo')
    intervalo = request.args.get('intervalo', '1d')
    resultado = get_historico(ticker, periodo, intervalo)
    status = 200 if resultado['ok'] else 500
    return jsonify(resultado), status
