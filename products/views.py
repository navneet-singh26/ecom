from django.http import HttpResponse
from rest_framework.decorators import api_view
import pandas as pd
from .models import Product


@api_view(['GET'])
def summary_report(request):
    action = request.query_params.get('action')

    df = pd.DataFrame(list(Product.objects.all().values()))

    summary = df.groupby('category').agg(
        total_revenue=pd.NamedAgg(column='price', aggfunc='sum'),
        top_product=pd.NamedAgg(column='product_name', aggfunc=lambda x: x.loc[df.loc[x.index, 'quantity_sold'].idxmax()]),
        top_product_quantity_sold=pd.NamedAgg(column='quantity_sold', aggfunc='max')
    ).reset_index()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=summary_report.csv'
    summary.to_csv(response, index=False)

    return response
