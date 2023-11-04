from main import app
from views import AdsView

ads_view = AdsView.as_view('ads')

app.add_url_rule('/ads/', view_func=ads_view, methods=['POST'])
app.add_url_rule('/ads/<int:ads_id>/', view_func=ads_view, methods=['GET', 'PATCH', 'DELETE'])