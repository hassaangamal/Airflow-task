# simulators/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def calculate_kpi(request):
    """
    Endpoint to calculate KPI based on input value
    """
    try:
        value = request.data.get('value')
        kpi_id = request.data.get('kpi_id')
        
        if value is None or kpi_id is None:
            return Response(
                {'error': 'Both value and kpi_id are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Example KPI calculations based on kpi_id
        if kpi_id == 1:
            result = float(value) * 1.5  # Example: 50% increase
        elif kpi_id == 2:
            result = float(value) * 0.8  # Example: 20% decrease
        else:
            result = float(value)  # Default: no change
            
        return Response({
            'kpi_id': kpi_id,
            'input_value': value,
            'result': result
        })
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )