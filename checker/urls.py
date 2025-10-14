Try AI directly in your favorite apps … Use Gemini to generate drafts and refine content, plus get Gemini Pro with access to Google's next-gen AI for BDT 2,500 BDT 0 for 1 month
from django.urls import path
from . import views

app_name = 'checker'

urlpatterns = [
    path('', views.EntryListView.as_view(), name='entry_list'),
    path('entry/<int:pk>/', views.EntryDetailView.as_view(), name='entry_detail'),
    path('entry/add/', views.EntryCreateView.as_view(), name='entry_add'),
    path('entry/<int:pk>/edit/', views.EntryUpdateView.as_view(), name='entry_edit'),
    path('entry/<int:pk>/delete/', views.EntryDeleteView.as_view(), name='entry_delete'),
    path('compare/', views.compare_view, name='compare'),
    path('history/', views.ComparisonHistoryListView.as_view(), name='history_list'),
    path('history/<int:pk>/', views.ComparisonHistoryDetailView.as_view(), name='history_detail'),
    path('history/<int:pk>/delete/', views.ComparisonHistoryDeleteView.as_view(), name='history_delete'),
]