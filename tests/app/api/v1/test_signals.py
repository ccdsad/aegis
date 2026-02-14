from httpx import AsyncClient


class TestSignalsPipeline:
    async def test_process_signal_approved(self, client: AsyncClient) -> None:
        response = await client.post(
            '/api/v1/signals',
            json={
                'signal': {
                    'strategy_id': 's1',
                    'symbol': 'BTCUSDT',
                    'side': 'buy',
                    'signal_type': 'entry',
                    'quantity': 1.0,
                },
                'market_state': {'prices': {'BTCUSDT': 100.0}},
                'risk_state': {'drawdown': 0.01},
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data['approved'] is True
        assert data['reason'] == 'ok'
        assert len(data['fills']) == 1

    async def test_process_signal_rejected(self, client: AsyncClient) -> None:
        response = await client.post(
            '/api/v1/signals',
            json={
                'signal': {
                    'strategy_id': 's1',
                    'symbol': 'BTCUSDT',
                    'side': 'buy',
                    'signal_type': 'entry',
                    'quantity': 10_000.0,
                },
                'market_state': {'prices': {'BTCUSDT': 100.0}},
                'risk_state': {'drawdown': 0.01},
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data['approved'] is False
        assert data['reason'] == 'limit_exceeded'
        assert data['fills'] == []

    async def test_get_order_audit_and_risk_decision(self, client: AsyncClient) -> None:
        process_response = await client.post(
            '/api/v1/signals',
            json={
                'signal': {
                    'strategy_id': 's1',
                    'symbol': 'BTCUSDT',
                    'side': 'buy',
                    'signal_type': 'entry',
                    'quantity': 1.0,
                },
                'market_state': {'prices': {'BTCUSDT': 100.0}},
                'risk_state': {'drawdown': 0.01},
            },
        )
        intent_uid = process_response.json()['intent_uid']

        order_response = await client.get(f'/api/v1/orders/{intent_uid}')
        risk_response = await client.get(f'/api/v1/risk/decisions/{intent_uid}')

        assert order_response.status_code == 200
        assert risk_response.status_code == 200
        assert order_response.json()['uid'] == intent_uid
        assert risk_response.json()['intent_uid'] == intent_uid

    async def test_get_strategy_status(self, client: AsyncClient) -> None:
        response = await client.get('/api/v1/strategies/s1/status')

        assert response.status_code == 200
        data = response.json()
        assert data['strategy_id'] == 's1'
        assert data['enabled'] is True
