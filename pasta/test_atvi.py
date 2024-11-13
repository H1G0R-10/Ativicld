import pytest
from unittest import mock
from requests.models import Response
import requests
from io import StringIO


class BancoDeDados:
    def buscar_pedido(self, pedido_id):
        raise NotImplementedError("Consulta real ao banco de dados")

def calcular_valor_total(pedido_id):
    resposta = requests.get(f"http://api.loja.com/pedidos/{pedido_id}")
    dados_produtos = resposta.json()
    
    total = sum(item["preco"] * item["quantidade"] for item in dados_produtos)
    return total

def obter_pedido_com_valor_total(pedido_id, banco):
    pedido = banco.buscar_pedido(pedido_id)
    valor_total = calcular_valor_total(pedido_id)
    pedido["valor_total"] = valor_total
    return pedido


@pytest.fixture
def mock_banco():
    banco_mock = mock.Mock(spec=BancoDeDados)
    banco_mock.buscar_pedido.return_value = {"id": 1, "cliente": "João"}
    return banco_mock

@pytest.fixture
def mock_resposta_api():
    resposta_mock = mock.Mock(spec=Response)
    resposta_mock.json.return_value = [
        {"preco": 100.0, "quantidade": 2},
        {"preco": 50.0, "quantidade": 1}
    ]
    return resposta_mock


# Testes

def test_calcular_valor_total(mock_resposta_api):
    with mock.patch("requests.get", return_value=mock_resposta_api):
        total = calcular_valor_total(1)
        assert total == 250.0, f"Valor total esperado: 250.0, mas obteve: {total}"

def test_obter_pedido_com_valor_total(mock_banco, mock_resposta_api):
    with mock.patch("requests.get", return_value=mock_resposta_api):
        pedido = obter_pedido_com_valor_total(1, mock_banco)
        assert pedido["id"] == 1, "ID do pedido não corresponde."
        assert pedido["cliente"] == "João", "Cliente do pedido não corresponde."
        assert pedido["valor_total"] == 250.0, f"Valor total esperado: 250.0, mas obteve: {pedido['valor_total']}"


if __name__ == "__main__":
    pytest.main()
