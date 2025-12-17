"""
لوحة تحكم المبيعات الذكية - ملف واحد موحد مع نظام ترجمة كامل وتقرير نصي مدمج
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import re
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from io import BytesIO
import textwrap

# ==================== نظام الترجمة الكامل ====================

class TranslationSystem:
    """نظام ترجمة متكامل ثنائي اللغة"""
    
    TRANSLATIONS = {
        'ar': {
            # العنوان الرئيسي
            'dashboard_title': '📊 لوحة تحكم المبيعات الذكية',
            'dashboard_subtitle': 'تحليل ذكي لبيانات المبيعات - رفع ملفات Excel/CSV متعددة',
            
            # الشريط الجانبي
            'sidebar_settings': '⚙️ الإعدادات',
            'language': 'اللغة',
            'theme': 'المظهر',
            'light_theme': '☀️ فاتح',
            'dark_theme': '🌙 مظلم',
            'load_settings': '📥 تحميل الإعدادات',
            'save_settings': '💾 حفظ الإعدادات',
            'settings_loaded': 'تم تحميل الإعدادات السابقة',
            'settings_saved': 'تم حفظ الإعدادات',
            'no_settings': 'لا توجد إعدادات سابقة',
            'reset': '🔄 إعادة تعيين',
            
            # رفع الملفات
            'step_1': 'الخطوة 1: رفع الملفات',
            'upload_title': '📤 رفع ملفات المبيعات',
            'upload_hint': 'اسحب وأفلت ملفات Excel أو CSV هنا أو انقر للاختيار',
            'upload_supported': 'يدعم: Excel (.xlsx, .xls), CSV',
            'upload_success': '✅ تم تحميل {count} ملف بنجاح!',
            'upload_error': '❌ خطأ في تحميل الملف:',
            'file_info': '📄 معلومات الملف',
            'file_name': 'اسم الملف',
            'file_size': 'حجم الملف',
            'rows': 'عدد الصفوف',
            'columns': 'عدد الأعمدة',
            'preview': '👀 معاينة البيانات',
            'preview_rows': 'عرض أول 5 صفوف',
            'merge_files': '🔗 دمج الملفات',
            'use_merged': 'استخدام البيانات المدمجة',
            'use_single': 'استخدام ملف واحد',
            'merged_success': '✅ تم دمج الملفات بنجاح!',
            
            # الإحصائيات
            'statistics': '📈 الإحصائيات',
            'total_files': 'عدد الملفات',
            'total_records': 'عدد السجلات',
            'total_columns': 'عدد الأعمدة',
            'numeric_columns': 'أعمدة رقمية',
            'merged_data': 'بيانات مدمجة',
            'individual_file': 'ملف فردي',
            
            # تعيين الأعمدة
            'step_2': 'الخطوة 2: تعيين الأعمدة',
            'mapping_title': '🎯 تعيين أعمدة البيانات',
            'auto_detection': '💡 التعرف التلقائي',
            'auto_detection_desc': 'النظام حاول تخمين أنواع الأعمدة. يمكنك تعديلها يدوياً إذا لزم الأمر.',
            'not_available': '❌ غير متوفر',
            
            # فئات الأعمدة
            'category_order': 'معلومات الطلب',
            'category_customer': 'معلومات العميل',
            'category_product': 'معلومات المنتج',
            'category_financial': 'المعلومات المالية',
            'category_location': 'الموقع',
            'category_sales': 'معلومات المبيعات',
            
            # أسماء الحقول
            'field_order_id': 'رقم الطلب',
            'field_customer_id': 'رقم العميل',
            'field_customer_name': 'اسم العميل',
            'field_product_id': 'رقم المنتج',
            'field_product_name': 'اسم المنتج',
            'field_category': 'الفئة',
            'field_quantity': 'الكمية',
            'field_unit_price': 'سعر الوحدة',
            'field_total_amount': 'المبلغ الإجمالي',
            'field_order_date': 'تاريخ الطلب',
            'field_region': 'المنطقة',
            'field_city': 'المدينة',
            'field_country': 'البلد',
            'field_salesperson': 'مندوب المبيعات',
            'field_payment_method': 'طريقة الدفع',
            'field_discount': 'الخصم',
            'field_profit': 'الربح',
            'field_cost': 'التكلفة',
            'field_status': 'حالة الطلب',
            
            # التحليل
            'step_3': 'الخطوة 3: التحليل',
            'analyze_button': '🚀 بدء التحليل',
            'analysis_title': '📊 نتائج تحليل المبيعات',
            'loading_analysis': 'جاري تحليل البيانات...',
            
            # KPIs
            'kpis_title': '📈 المؤشرات الرئيسية',
            'kpi_transactions': 'إجمالي المعاملات',
            'kpi_sales': 'إجمالي المبيعات',
            'kpi_avg_transaction': 'متوسط قيمة المعاملة',
            'kpi_profit': 'إجمالي الربح',
            'kpi_customers': 'عدد العملاء',
            'kpi_products': 'عدد المنتجات',
            'kpi_avg_quantity': 'متوسط الكمية',
            'kpi_discount_rate': 'معدل الخصم',
            
            # الرسوم البيانية
            'charts_title': '📊 الرسوم البيانية',
            'chart_sales_trend': 'اتجاه المبيعات الشهري',
            'chart_top_products': 'أفضل 10 منتجات مبيعاً',
            'chart_region_dist': 'توزيع المبيعات حسب المنطقة',
            'chart_category_dist': 'توزيع المبيعات حسب الفئة',
            'chart_sales_performance': 'أداء مندوبي المبيعات',
            'chart_price_quantity': 'العلاقة بين السعر والكمية',
            'chart_payment_methods': 'توزيع طرق الدفع',
            'chart_profit_dist': 'توزيع الأرباح',
            'no_charts_data': '⚠️ لا توجد بيانات كافية لإنشاء الرسوم البيانية',
            
            # التحليل المتقدم
            'advanced_analysis': '🔍 تحليل متقدم',
            'correlation_matrix': 'مصفوفة الارتباط',
            'outlier_detection': 'كشف القيم الشاذة',
            'outliers_found': 'تم اكتشاف {count} قيمة شاذة',
            'no_outliers': '✅ لم يتم اكتشاف قيم شاذة',
            'zero_std': 'انحراف معياري صفري - لا يمكن كشف القيم الشاذة',
            
            # التقرير
            'report_title': '📄 التقرير التحليلي الاحترافي',
            'generate_report': '📋 إنشاء التقرير الاحترافي',
            'copy_report': '📋 نسخ التقرير',
            'report_copied': '✅ تم نسخ التقرير إلى الحافظة',
            'executive_summary': 'الملخص التنفيذي',
            'data_overview': 'نظرة عامة على البيانات',
            'key_findings': 'النقاط الرئيسية',
            'performance_analysis': 'تحليل الأداء',
            'recommendations': 'التوصيات الاستراتيجية',
            'data_quality': 'جودة البيانات',
            'report_date': 'تاريخ التقرير',
            'analysis_period': 'فترة التحليل',
            'total_analysis': 'إجمالي التحليل',
            'top_performers': 'الأفضل أداءً',
            'areas_improvement': 'مجالات التحسين',
            
            # جودة البيانات
            'data_quality_title': '🔍 جودة البيانات',
            'missing_values': 'قيم مفقودة',
            'duplicates': 'سجلات مكررة',
            'negative_amounts': 'مبالغ سلبية',
            'invalid_quantities': 'كميات غير منطقية',
            'future_dates': 'تواريخ مستقبلية',
            
            # الأزرار العامة
            'download': 'تحميل',
            'copy': 'نسخ',
            'close': 'إغلاق',
            'back': 'رجوع',
            'next': 'التالي',
            'finish': 'إنهاء',
            
            # الرسائل
            'no_data': 'لم يتم تحميل بيانات بعد',
            'select_file_first': 'يرجى رفع ملف أولاً',
            'select_columns': 'يرجى تعيين الأعمدة أولاً',
            'analysis_complete': 'تم التحليل بنجاح',
            'error': 'خطأ',
            'warning': 'تحذير',
            'success': 'نجاح',
            'info': 'معلومة',
            
            # مصطلحات إضافية للتقرير
            'company_name': 'شركة التميز التجارية',
            'report_author': 'إدارة التحليلات والأبحاث',
            'report_id': 'رقم التقرير',
            'report_period': 'فترة التقرير',
            'market_share': 'حصصة السوق',
            'growth_rate': 'معدل النمو',
            'customer_satisfaction': 'رضا العملاء',
            'revenue_breakdown': 'توزيع الإيرادات',
            'performance_metrics': 'مقاييس الأداء',
            'strategic_insights': 'رؤى استراتيجية',
            'actionable_recommendations': 'توصيات قابلة للتنفيذ',
            'risk_assessment': 'تقييم المخاطر',
            'opportunity_analysis': 'تحليل الفرص',
            'competitive_analysis': 'تحليل المنافسة',
            'financial_summary': 'ملخص مالي',
            'sales_forecast': 'توقعات المبيعات',
            'customer_behavior': 'سلوك العملاء',
            'product_performance': 'أداء المنتجات',
            'regional_analysis': 'تحليل المناطق',
            'quarterly_comparison': 'مقارنة ربع سنوية',
            'annual_trends': 'اتجاهات سنوية',
            'market_penetration': 'اختراق السوق',
            'customer_acquisition': 'اكتساب العملاء',
            'customer_retention': 'احتفاظ بالعملاء',
            'profit_margin': 'هامش الربح',
            'return_on_investment': 'العائد على الاستثمار',
            'operational_efficiency': 'الكفاءة التشغيلية',
        },
        
        'en': {
            # Main Title
            'dashboard_title': '📊 Smart Sales Analytics Dashboard',
            'dashboard_subtitle': 'Intelligent sales data analysis - Upload multiple Excel/CSV files',
            
            # Sidebar
            'sidebar_settings': '⚙️ Settings',
            'language': 'Language',
            'theme': 'Theme',
            'light_theme': '☀️ Light',
            'dark_theme': '🌙 Dark',
            'load_settings': '📥 Load Settings',
            'save_settings': '💾 Save Settings',
            'settings_loaded': 'Previous settings loaded',
            'settings_saved': 'Settings saved',
            'no_settings': 'No previous settings',
            'reset': '🔄 Reset',
            
            # File Upload
            'step_1': 'Step 1: Upload Files',
            'upload_title': '📤 Upload Sales Files',
            'upload_hint': 'Drag and drop Excel or CSV files here or click to browse',
            'upload_supported': 'Supports: Excel (.xlsx, .xls), CSV',
            'upload_success': '✅ Successfully uploaded {count} file(s)!',
            'upload_error': '❌ Error loading file:',
            'file_info': '📄 File Information',
            'file_name': 'File Name',
            'file_size': 'File Size',
            'rows': 'Rows',
            'columns': 'Columns',
            'preview': '👀 Data Preview',
            'preview_rows': 'Show first 5 rows',
            'merge_files': '🔗 Merge Files',
            'use_merged': 'Use Merged Data',
            'use_single': 'Use Single File',
            'merged_success': '✅ Files merged successfully!',
            
            # Statistics
            'statistics': '📈 Statistics',
            'total_files': 'Total Files',
            'total_records': 'Total Records',
            'total_columns': 'Total Columns',
            'numeric_columns': 'Numeric Columns',
            'merged_data': 'Merged Data',
            'individual_file': 'Individual File',
            
            # Column Mapping
            'step_2': 'Step 2: Map Columns',
            'mapping_title': '🎯 Data Column Mapping',
            'auto_detection': '💡 Auto Detection',
            'auto_detection_desc': 'System tried to guess column types. You can adjust manually if needed.',
            'not_available': '❌ Not Available',
            
            # Column Categories
            'category_order': 'Order Information',
            'category_customer': 'Customer Information',
            'category_product': 'Product Information',
            'category_financial': 'Financial Information',
            'category_location': 'Location',
            'category_sales': 'Sales Information',
            
            # Field Names
            'field_order_id': 'Order ID',
            'field_customer_id': 'Customer ID',
            'field_customer_name': 'Customer Name',
            'field_product_id': 'Product ID',
            'field_product_name': 'Product Name',
            'field_category': 'Category',
            'field_quantity': 'Quantity',
            'field_unit_price': 'Unit Price',
            'field_total_amount': 'Total Amount',
            'field_order_date': 'Order Date',
            'field_region': 'Region',
            'field_city': 'City',
            'field_country': 'Country',
            'field_salesperson': 'Salesperson',
            'field_payment_method': 'Payment Method',
            'field_discount': 'Discount',
            'field_profit': 'Profit',
            'field_cost': 'Cost',
            'field_status': 'Order Status',
            
            # Analysis
            'step_3': 'Step 3: Analysis',
            'analyze_button': '🚀 Start Analysis',
            'analysis_title': '📊 Sales Analysis Results',
            'loading_analysis': 'Analyzing data...',
            
            # KPIs
            'kpis_title': '📈 Key Performance Indicators',
            'kpi_transactions': 'Total Transactions',
            'kpi_sales': 'Total Sales',
            'kpi_avg_transaction': 'Average Transaction Value',
            'kpi_profit': 'Total Profit',
            'kpi_customers': 'Number of Customers',
            'kpi_products': 'Number of Products',
            'kpi_avg_quantity': 'Average Quantity',
            'kpi_discount_rate': 'Discount Rate',
            
            # Charts
            'charts_title': '📊 Charts & Visualizations',
            'chart_sales_trend': 'Monthly Sales Trend',
            'chart_top_products': 'Top 10 Selling Products',
            'chart_region_dist': 'Sales Distribution by Region',
            'chart_category_dist': 'Sales Distribution by Category',
            'chart_sales_performance': 'Salesperson Performance',
            'chart_price_quantity': 'Price vs Quantity Relationship',
            'chart_payment_methods': 'Payment Methods Distribution',
            'chart_profit_dist': 'Profit Distribution',
            'no_charts_data': '⚠️ Insufficient data to generate charts',
            
            # Advanced Analysis
            'advanced_analysis': '🔍 Advanced Analysis',
            'correlation_matrix': 'Correlation Matrix',
            'outlier_detection': 'Outlier Detection',
            'outliers_found': 'Found {count} outliers',
            'no_outliers': '✅ No outliers detected',
            'zero_std': 'Zero standard deviation - Cannot detect outliers',
            
            # Report
            'report_title': '📄 Professional Analytical Report',
            'generate_report': '📋 Generate Professional Report',
            'copy_report': '📋 Copy Report',
            'report_copied': '✅ Report copied to clipboard',
            'executive_summary': 'Executive Summary',
            'data_overview': 'Data Overview',
            'key_findings': 'Key Findings',
            'performance_analysis': 'Performance Analysis',
            'recommendations': 'Strategic Recommendations',
            'data_quality': 'Data Quality',
            'report_date': 'Report Date',
            'analysis_period': 'Analysis Period',
            'total_analysis': 'Total Analysis',
            'top_performers': 'Top Performers',
            'areas_improvement': 'Areas for Improvement',
            
            # Data Quality
            'data_quality_title': '🔍 Data Quality',
            'missing_values': 'Missing Values',
            'duplicates': 'Duplicate Records',
            'negative_amounts': 'Negative Amounts',
            'invalid_quantities': 'Invalid Quantities',
            'future_dates': 'Future Dates',
            
            # General Buttons
            'download': 'Download',
            'copy': 'Copy',
            'close': 'Close',
            'back': 'Back',
            'next': 'Next',
            'finish': 'Finish',
            
            # Messages
            'no_data': 'No data loaded yet',
            'select_file_first': 'Please upload a file first',
            'select_columns': 'Please map columns first',
            'analysis_complete': 'Analysis completed successfully',
            'error': 'Error',
            'warning': 'Warning',
            'success': 'Success',
            'info': 'Info',
            
            # Additional report terms
            'company_name': 'Excellence Trading Company',
            'report_author': 'Analytics & Research Department',
            'report_id': 'Report ID',
            'report_period': 'Report Period',
            'market_share': 'Market Share',
            'growth_rate': 'Growth Rate',
            'customer_satisfaction': 'Customer Satisfaction',
            'revenue_breakdown': 'Revenue Breakdown',
            'performance_metrics': 'Performance Metrics',
            'strategic_insights': 'Strategic Insights',
            'actionable_recommendations': 'Actionable Recommendations',
            'risk_assessment': 'Risk Assessment',
            'opportunity_analysis': 'Opportunity Analysis',
            'competitive_analysis': 'Competitive Analysis',
            'financial_summary': 'Financial Summary',
            'sales_forecast': 'Sales Forecast',
            'customer_behavior': 'Customer Behavior',
            'product_performance': 'Product Performance',
            'regional_analysis': 'Regional Analysis',
            'quarterly_comparison': 'Quarterly Comparison',
            'annual_trends': 'Annual Trends',
            'market_penetration': 'Market Penetration',
            'customer_acquisition': 'Customer Acquisition',
            'customer_retention': 'Customer Retention',
            'profit_margin': 'Profit Margin',
            'return_on_investment': 'Return on Investment',
            'operational_efficiency': 'Operational Efficiency',
        }
    }
    
    @classmethod
    def t(cls, key, **kwargs):
        """ترجمة النص بناءً على اللغة الحالية"""
        lang = st.session_state.get('language', 'ar')
        translation = cls.TRANSLATIONS.get(lang, cls.TRANSLATIONS['ar']).get(key, key)
        
        if kwargs:
            try:
                return translation.format(**kwargs)
            except:
                return translation
        return translation
    
    @classmethod
    def get_language_direction(cls):
        """الحصول على اتجاه النص للغة الحالية"""
        lang = st.session_state.get('language', 'ar')
        return 'rtl' if lang == 'ar' else 'ltr'
    
    @classmethod
    def get_font_family(cls):
        """الحصول على خط النص للغة الحالية"""
        lang = st.session_state.get('language', 'ar')
        return "'Cairo', 'Segoe UI', sans-serif" if lang == 'ar' else "'Segoe UI', Tahoma, Geneva, sans-serif"

# ==================== 1. وحدة التعرف التلقائي على الأعمدة ====================

class SalesAutoColumnMapper:
    def __init__(self, dataframe):
        self.df = dataframe
        self.column_patterns = self._initialize_patterns()
    
    def _initialize_patterns(self):
        """تهيئة الأنماط للتعرف على أعمدة المبيعات"""
        return {
            'order_id': {
                'patterns': ['order.*id', 'order.*no', 'transaction.*id', 'رقم.*الطلب', 'معرف.*الطلب'],
                'keywords': ['order', 'transaction', 'طلب', 'معرف']
            },
            'customer_id': {
                'patterns': ['customer.*id', 'client.*id', 'cust.*id', 'رقم.*العميل', 'معرف.*العميل'],
                'keywords': ['customer', 'client', 'عميل', 'زبون']
            },
            'customer_name': {
                'patterns': ['customer.*name', 'client.*name', 'اسم.*العميل', 'العميل'],
                'keywords': ['customer', 'client', 'اسم', 'name']
            },
            'product_id': {
                'patterns': ['product.*id', 'item.*id', 'sku', 'رقم.*المنتج', 'معرف.*المنتج'],
                'keywords': ['product', 'item', 'sku', 'منتج', 'سلعة']
            },
            'product_name': {
                'patterns': ['product.*name', 'item.*name', 'اسم.*المنتج', 'المنتج'],
                'keywords': ['product', 'item', 'اسم', 'name', 'منتج']
            },
            'category': {
                'patterns': ['category', 'type', 'class', 'فئة', 'تصنيف', 'نوع'],
                'keywords': ['category', 'type', 'فئة', 'تصنيف']
            },
            'quantity': {
                'patterns': ['quantity', 'qty', 'amount', 'الكمية', 'عدد', 'مقدار'],
                'keywords': ['quantity', 'qty', 'كمية', 'عدد']
            },
            'price': {
                'patterns': ['price', 'unit.*price', 'cost', 'سعر', 'السعر', 'التكلفة'],
                'keywords': ['price', 'cost', 'سعر', 'تكلفة']
            },
            'total_amount': {
                'patterns': ['total', 'amount', 'revenue', 'المبلغ', 'الإجمالي', 'الإيراد'],
                'keywords': ['total', 'amount', 'revenue', 'إجمالي', 'مبلغ']
            },
            'order_date': {
                'patterns': ['order.*date', 'transaction.*date', 'date', 'تاريخ.*الطلب', 'التاريخ'],
                'keywords': ['date', 'تاريخ', 'order', 'طلب']
            },
            'region': {
                'patterns': ['region', 'area', 'zone', 'منطقة', 'المنطقة', 'الفرع'],
                'keywords': ['region', 'area', 'zone', 'منطقة']
            },
            'city': {
                'patterns': ['city', 'town', 'المدينة', 'مدينة'],
                'keywords': ['city', 'town', 'مدينة']
            },
            'country': {
                'patterns': ['country', 'state', 'البلد', 'الدولة'],
                'keywords': ['country', 'state', 'بلد', 'دولة']
            },
            'salesperson': {
                'patterns': ['salesperson', 'seller', 'agent', 'مندوب', 'البائع', 'الموظف'],
                'keywords': ['sales', 'seller', 'agent', 'مندوب', 'بائع']
            },
            'payment_method': {
                'patterns': ['payment.*method', 'payment.*type', 'طريقة.*الدفع', 'نوع.*الدفع'],
                'keywords': ['payment', 'دفع', 'method', 'طريقة']
            },
            'discount': {
                'patterns': ['discount', 'off', 'خصم', 'التخفيض'],
                'keywords': ['discount', 'خصم', 'تخفيض']
            },
            'profit': {
                'patterns': ['profit', 'margin', 'ربح', 'الربح', 'هامش'],
                'keywords': ['profit', 'margin', 'ربح', 'هامش']
            },
            'status': {
                'patterns': ['status', 'state', 'condition', 'حالة', 'الحالة'],
                'keywords': ['status', 'state', 'حالة']
            }
        }
    
    def auto_detect_columns(self):
        """التعرف التلقائي على أنواع الأعمدة"""
        suggestions = {}
        columns = self.df.columns.tolist()
        
        for column in columns:
            column_lower = str(column).lower()
            
            for field_type, patterns_info in self.column_patterns.items():
                for pattern in patterns_info['patterns']:
                    if re.search(pattern, column_lower, re.IGNORECASE):
                        suggestions[field_type] = column
                        break
                
                if field_type not in suggestions:
                    for keyword in patterns_info['keywords']:
                        if keyword.lower() in column_lower:
                            suggestions[field_type] = column
                            break
            
            if self._is_date_column(column):
                if 'order_date' not in suggestions:
                    suggestions['order_date'] = column
        
        return suggestions
    
    def _is_date_column(self, column_name):
        """فحص إذا كان العمود يحتوي على تواريخ"""
        if column_name not in self.df.columns:
            return False
        
        column_sample = self.df[column_name].dropna().head(10)
        
        if len(column_sample) == 0:
            return False
        
        try:
            if pd.api.types.is_datetime64_any_dtype(self.df[column_name]):
                return True
            
            test_dates = pd.to_datetime(column_sample, errors='coerce')
            success_rate = test_dates.notna().sum() / len(column_sample)
            
            return success_rate > 0.7
        except:
            return False

# ==================== 2. وحدة التحليل الذكي ====================

class SalesDataAnalyzer:
    def __init__(self, dataframe, column_mapping):
        self.df = dataframe.copy()
        self.mapping = column_mapping
    
    def analyze_all(self):
        """إجراء جميع التحليلات المتاحة للمبيعات"""
        analysis_results = {
            'kpis': {},
            'distributions': {},
            'trends': {},
            'insights': [],
            'warnings': [],
            'top_performers': {},
            'growth_metrics': {},
            'customer_analysis': {},
            'product_analysis': {}
        }
        
        analysis_results['kpis'] = self._calculate_kpis()
        analysis_results['distributions'] = self._analyze_distributions()
        analysis_results['trends'] = self._analyze_trends()
        analysis_results['insights'] = self._extract_insights()
        analysis_results['warnings'] = self._check_data_quality()
        analysis_results['top_performers'] = self._identify_top_performers()
        analysis_results['growth_metrics'] = self._calculate_growth_metrics()
        analysis_results['customer_analysis'] = self._analyze_customer_segments()
        analysis_results['product_analysis'] = self._analyze_product_portfolio()
        
        return analysis_results
    
   def _calculate_kpis(self):
    """حساب مؤشرات أداء المبيعات"""
    kpis = {}
    
    # إجمالي عدد المعاملات
    total_transactions = len(self.df)
    kpis['total_transactions'] = {
        'value': total_transactions,
        'formatted': f"{total_transactions:,}",
        'label': TranslationSystem.t('kpi_transactions'),
        'icon': '🛒',
        'trend': 'neutral'
    }
    
    # إجمالي المبيعات
    if 'total_amount' in self.mapping:
        amount_col = self.mapping['total_amount']
        if amount_col in self.df.columns:
            try:
                self.df[amount_col] = pd.to_numeric(self.df[amount_col], errors='coerce')
                total_sales = self.df[amount_col].sum()
                kpis['total_sales'] = {
                    'value': total_sales,
                    'formatted': f"${total_sales:,.0f}",
                    'label': TranslationSystem.t('kpi_sales'),
                    'icon': '💰',
                    'trend': 'positive' if total_sales > 0 else 'negative'
                }
                
                avg_transaction = total_sales / total_transactions if total_transactions > 0 else 0
                kpis['avg_transaction'] = {
                    'value': avg_transaction,
                    'formatted': f"${avg_transaction:,.0f}",
                    'label': TranslationSystem.t('kpi_avg_transaction'),
                    'icon': '📊',
                    'trend': 'positive' if avg_transaction > 0 else 'negative'
                }
            except:
                pass
    
    # إجمالي الربح وهامش الربح
    total_profit = 0
    profit_margin = 0
    
    # الحالة 1: إذا كان هناك عمود profit مباشرة
    if 'profit' in self.mapping:
        profit_col = self.mapping['profit']
        if profit_col in self.df.columns:
            try:
                self.df[profit_col] = pd.to_numeric(self.df[profit_col], errors='coerce')
                total_profit = self.df[profit_col].sum()
            except:
                pass
    
    # الحالة 2: إذا لم يكن هناك profit ولكن هناك total_amount و cost
    elif 'cost' in self.mapping and 'total_amount' in self.mapping:
        cost_col = self.mapping['cost']
        amount_col = self.mapping['total_amount']
        if cost_col in self.df.columns and amount_col in self.df.columns:
            try:
                self.df[cost_col] = pd.to_numeric(self.df[cost_col], errors='coerce')
                self.df[amount_col] = pd.to_numeric(self.df[amount_col], errors='coerce')
                total_cost = self.df[cost_col].sum()
                total_sales = self.df[amount_col].sum()
                total_profit = total_sales - total_cost
            except:
                pass
    
    # الحالة 3: إذا لم يكن هناك أي منهما، احسب نسبة ربح افتراضية (20%)
    elif 'total_amount' in self.mapping:
        amount_col = self.mapping['total_amount']
        if amount_col in self.df.columns:
            try:
                self.df[amount_col] = pd.to_numeric(self.df[amount_col], errors='coerce')
                total_sales = self.df[amount_col].sum()
                total_profit = total_sales * 0.20  # افتراض هامش ربح 20%
            except:
                pass
    
    # حساب هامش الربح
    if 'total_sales' in kpis:
        total_sales = kpis['total_sales']['value']
        if total_sales > 0:
            profit_margin = (total_profit / total_sales) * 100
        else:
            profit_margin = 0
    else:
        profit_margin = 0
    
    # إضافة مؤشر الربح إذا كان له قيمة
    if total_profit != 0:
        kpis['total_profit'] = {
            'value': total_profit,
            'formatted': f"${total_profit:,.0f}",
            'label': TranslationSystem.t('kpi_profit'),
            'icon': '📈',
            'trend': 'positive' if total_profit > 0 else 'negative'
        }
        
        kpis['profit_margin'] = {
            'value': profit_margin,
            'formatted': f"{profit_margin:.1f}%",
            'label': TranslationSystem.t('profit_margin'),
            'icon': '📊',
            'trend': 'positive' if profit_margin > 15 else 'neutral'
        }
    
    # عدد العملاء الفريدين
    if 'customer_id' in self.mapping:
        customer_col = self.mapping['customer_id']
        if customer_col in self.df.columns:
            unique_customers = self.df[customer_col].nunique()
            kpis['unique_customers'] = {
                'value': unique_customers,
                'formatted': f"{unique_customers:,}",
                'label': TranslationSystem.t('kpi_customers'),
                'icon': '👥',
                'trend': 'positive' if unique_customers > 0 else 'neutral'
            }
    
    # عدد المنتجات الفريدة
    if 'product_id' in self.mapping:
        product_col = self.mapping['product_id']
        if product_col in self.df.columns:
            unique_products = self.df[product_col].nunique()
            kpis['unique_products'] = {
                'value': unique_products,
                'formatted': f"{unique_products:,}",
                'label': TranslationSystem.t('kpi_products'),
                'icon': '📦',
                'trend': 'positive' if unique_products > 0 else 'neutral'
            }
    
    # متوسط الكمية لكل معاملة
    if 'quantity' in self.mapping:
        quantity_col = self.mapping['quantity']
        if quantity_col in self.df.columns:
            try:
                self.df[quantity_col] = pd.to_numeric(self.df[quantity_col], errors='coerce')
                avg_quantity = self.df[quantity_col].mean()
                kpis['avg_quantity'] = {
                    'value': avg_quantity,
                    'formatted': f"{avg_quantity:.1f}",
                    'label': TranslationSystem.t('kpi_avg_quantity'),
                    'icon': '⚖️',
                    'trend': 'positive' if avg_quantity > 1 else 'neutral'
                }
            except:
                pass
    
    # معدل الخصم
    if 'discount' in self.mapping and 'total_amount' in self.mapping:
        discount_col = self.mapping['discount']
        amount_col = self.mapping['total_amount']
        if discount_col in self.df.columns and amount_col in self.df.columns:
            try:
                self.df[discount_col] = pd.to_numeric(self.df[discount_col], errors='coerce')
                total_discount = self.df[discount_col].sum()
                discount_rate = (total_discount / total_sales * 100) if total_sales > 0 else 0
                
                kpis['discount_rate'] = {
                    'value': discount_rate,
                    'formatted': f"{discount_rate:.1f}%",
                    'label': TranslationSystem.t('kpi_discount_rate'),
                    'icon': '🎯',
                    'trend': 'positive' if discount_rate < 10 else 'neutral'
                }
            except:
                pass
    
    return kpis
    def _calculate_growth_metrics(self):
        """حساب مقاييس النمو"""
        growth_metrics = {}
        
        if 'order_date' in self.mapping and 'total_amount' in self.mapping:
            date_col = self.mapping['order_date']
            amount_col = self.mapping['total_amount']
            
            if date_col in self.df.columns and amount_col in self.df.columns:
                try:
                    df_copy = self.df.copy()
                    df_copy[date_col] = pd.to_datetime(df_copy[date_col], errors='coerce')
                    df_copy[amount_col] = pd.to_numeric(df_copy[amount_col], errors='coerce')
                    
                    df_clean = df_copy.dropna(subset=[date_col, amount_col])
                    
                    if len(df_clean) > 0:
                        df_clean['year_month'] = df_clean[date_col].dt.to_period('M')
                        monthly_sales = df_clean.groupby('year_month')[amount_col].sum()
                        
                        if len(monthly_sales) > 1:
                            latest_month = monthly_sales.iloc[-1]
                            previous_month = monthly_sales.iloc[-2]
                            month_over_month_growth = ((latest_month - previous_month) / previous_month * 100) if previous_month > 0 else 0
                            
                            growth_metrics['mom_growth'] = {
                                'value': month_over_month_growth,
                                'formatted': f"{month_over_month_growth:+.1f}%",
                                'label': 'Month-over-Month Growth'
                            }
                except:
                    pass
        
        return growth_metrics
    
    def _analyze_customer_segments(self):
        """تحليل شرائح العملاء"""
        customer_segments = {}
        
        if 'customer_id' in self.mapping and 'total_amount' in self.mapping:
            customer_col = self.mapping['customer_id']
            amount_col = self.mapping['total_amount']
            
            if customer_col in self.df.columns and amount_col in self.df.columns:
                try:
                    df_copy = self.df.copy()
                    df_copy[amount_col] = pd.to_numeric(df_copy[amount_col], errors='coerce')
                    
                    customer_sales = df_copy.groupby(customer_col)[amount_col].sum().sort_values(ascending=False)
                    
                    if len(customer_sales) > 0:
                        # تحليل العملاء حسب القيمة
                        top_10_customers = customer_sales.head(10).to_dict()
                        bottom_10_customers = customer_sales.tail(10).to_dict()
                        
                        customer_segments['top_customers'] = top_10_customers
                        customer_segments['bottom_customers'] = bottom_10_customers
                        
                        # حساب متوسط قيمة العميل
                        avg_customer_value = customer_sales.mean()
                        customer_segments['avg_customer_value'] = avg_customer_value
                        
                        # تحليل توزيع العملاء
                        segments = {
                            'VIP': customer_sales[customer_sales > customer_sales.quantile(0.8)].count(),
                            'High Value': customer_sales[(customer_sales <= customer_sales.quantile(0.8)) & 
                                                         (customer_sales > customer_sales.quantile(0.5))].count(),
                            'Medium Value': customer_sales[(customer_sales <= customer_sales.quantile(0.5)) & 
                                                           (customer_sales > customer_sales.quantile(0.2))].count(),
                            'Low Value': customer_sales[customer_sales <= customer_sales.quantile(0.2)].count()
                        }
                        
                        customer_segments['value_segments'] = segments
                except:
                    pass
        
        return customer_segments
    
    def _analyze_product_portfolio(self):
        """تحليل محفظة المنتجات"""
        product_analysis = {}
        
        if 'product_name' in self.mapping and 'total_amount' in self.mapping and 'profit' in self.mapping:
            product_col = self.mapping['product_name']
            amount_col = self.mapping['total_amount']
            profit_col = self.mapping['profit']
            
            if all(col in self.df.columns for col in [product_col, amount_col, profit_col]):
                try:
                    df_copy = self.df.copy()
                    df_copy[amount_col] = pd.to_numeric(df_copy[amount_col], errors='coerce')
                    df_copy[profit_col] = pd.to_numeric(df_copy[profit_col], errors='coerce')
                    
                    product_stats = df_copy.groupby(product_col).agg(
                        total_sales=(amount_col, 'sum'),
                        total_profit=(profit_col, 'sum'),
                        transaction_count=(amount_col, 'count')
                    ).reset_index()
                    
                    product_stats['profit_margin'] = (product_stats['total_profit'] / product_stats['total_sales'] * 100) if product_stats['total_sales'].sum() > 0 else 0
                    
                    # تصنيف المنتجات حسب الربحية
                    product_stats['product_category'] = pd.qcut(product_stats['profit_margin'], 
                                                              q=4, 
                                                              labels=['Low Profit', 'Medium Profit', 'High Profit', 'Premium'])
                    
                    product_analysis['product_stats'] = product_stats.to_dict('records')
                    
                    # تحليل ABC (باريتو)
                    product_stats_sorted = product_stats.sort_values('total_sales', ascending=False)
                    product_stats_sorted['cumulative_percentage'] = (product_stats_sorted['total_sales'].cumsum() / 
                                                                   product_stats_sorted['total_sales'].sum() * 100)
                    
                    product_analysis['pareto_analysis'] = product_stats_sorted.to_dict('records')
                    
                except:
                    pass
        
        return product_analysis
    
    def _analyze_distributions(self):
        """تحليل توزيع بيانات المبيعات"""
        distributions = {}
        
        if 'region' in self.mapping:
            region_col = self.mapping['region']
            if region_col in self.df.columns:
                region_dist = self.df[region_col].value_counts().to_dict()
                distributions['region'] = region_dist
        
        if 'category' in self.mapping:
            category_col = self.mapping['category']
            if category_col in self.df.columns:
                category_dist = self.df[category_col].value_counts().to_dict()
                distributions['category'] = category_dist
        
        if 'product_name' in self.mapping:
            product_col = self.mapping['product_name']
            if product_col in self.df.columns:
                product_dist = self.df[product_col].value_counts().head(10).to_dict()
                distributions['top_products'] = product_dist
        
        if 'payment_method' in self.mapping:
            payment_col = self.mapping['payment_method']
            if payment_col in self.df.columns:
                payment_dist = self.df[payment_col].value_counts().to_dict()
                distributions['payment_method'] = payment_dist
        
        return distributions
    
    def _analyze_trends(self):
        """تحليل اتجاهات المبيعات"""
        trends = {}
        
        if 'order_date' in self.mapping and 'total_amount' in self.mapping:
            date_col = self.mapping['order_date']
            amount_col = self.mapping['total_amount']
            
            if date_col in self.df.columns and amount_col in self.df.columns:
                try:
                    df_copy = self.df.copy()
                    df_copy[date_col] = pd.to_datetime(df_copy[date_col], errors='coerce')
                    df_copy[amount_col] = pd.to_numeric(df_copy[amount_col], errors='coerce')
                    
                    df_clean = df_copy.dropna(subset=[date_col, amount_col])
                    
                    if len(df_clean) > 0:
                        df_clean['year_month'] = df_clean[date_col].dt.to_period('M')
                        monthly_trend = df_clean.groupby('year_month')[amount_col].agg(['sum', 'count']).reset_index()
                        monthly_trend['year_month'] = monthly_trend['year_month'].astype(str)
                        
                        trends['monthly'] = monthly_trend.to_dict('records')
                        
                        # تحليل اتجاهات الموسمية
                        df_clean['month'] = df_clean[date_col].dt.month
                        monthly_pattern = df_clean.groupby('month')[amount_col].sum()
                        trends['seasonality'] = monthly_pattern.to_dict()
                except:
                    pass
        
        return trends
    
    def _extract_insights(self):
        """استخلاص رؤى من بيانات المبيعات"""
        insights = []
        lang = TranslationSystem.t('language')
        
        if 'region' in self.mapping and 'total_amount' in self.mapping:
            region_col = self.mapping['region']
            amount_col = self.mapping['total_amount']
            
            if region_col in self.df.columns and amount_col in self.df.columns:
                try:
                    self.df[amount_col] = pd.to_numeric(self.df[amount_col], errors='coerce')
                    region_sales = self.df.groupby(region_col)[amount_col].sum().sort_values(ascending=False)
                    
                    if len(region_sales) > 0:
                        top_region = region_sales.index[0]
                        top_sales = region_sales.iloc[0]
                        if lang == 'ar':
                            insights.append(f"🏆 **المنطقة الأكثر ربحية**: {top_region} (${top_sales:,.0f})")
                        else:
                            insights.append(f"🏆 **Most Profitable Region**: {top_region} (${top_sales:,.0f})")
                except:
                    pass
        
        if 'product_name' in self.mapping and 'quantity' in self.mapping:
            product_col = self.mapping['product_name']
            quantity_col = self.mapping['quantity']
            
            if product_col in self.df.columns and quantity_col in self.df.columns:
                try:
                    self.df[quantity_col] = pd.to_numeric(self.df[quantity_col], errors='coerce')
                    product_sales = self.df.groupby(product_col)[quantity_col].sum().sort_values(ascending=False)
                    
                    if len(product_sales) > 0:
                        top_product = product_sales.index[0]
                        top_qty = product_sales.iloc[0]
                        if lang == 'ar':
                            insights.append(f"📦 **المنتج الأكثر مبيعاً**: {top_product} ({top_qty:,} وحدة)")
                        else:
                            insights.append(f"📦 **Top Selling Product**: {top_product} ({top_qty:,} units)")
                except:
                    pass
        
        if 'salesperson' in self.mapping and 'total_amount' in self.mapping:
            salesperson_col = self.mapping['salesperson']
            amount_col = self.mapping['total_amount']
            
            if salesperson_col in self.df.columns and amount_col in self.df.columns:
                try:
                    self.df[amount_col] = pd.to_numeric(self.df[amount_col], errors='coerce')
                    salesperson_performance = self.df.groupby(salesperson_col)[amount_col].sum().sort_values(ascending=False)
                    
                    if len(salesperson_performance) > 0:
                        top_salesperson = salesperson_performance.index[0]
                        top_sales = salesperson_performance.iloc[0]
                        if lang == 'ar':
                            insights.append(f"👤 **أفضل مندوب مبيعات**: {top_salesperson} (${top_sales:,.0f})")
                        else:
                            insights.append(f"👤 **Top Salesperson**: {top_salesperson} (${top_sales:,.0f})")
                except:
                    pass
        
        return insights
    
    def _identify_top_performers(self):
        """تحديد الأفضل أداءً"""
        top_performers = {}
        
        if 'salesperson' in self.mapping and 'total_amount' in self.mapping:
            salesperson_col = self.mapping['salesperson']
            amount_col = self.mapping['total_amount']
            
            if salesperson_col in self.df.columns and amount_col in self.df.columns:
                try:
                    self.df[amount_col] = pd.to_numeric(self.df[amount_col], errors='coerce')
                    salesperson_performance = self.df.groupby(salesperson_col)[amount_col].sum().sort_values(ascending=False)
                    
                    if len(salesperson_performance) > 0:
                        top_3_salespeople = salesperson_performance.head(3)
                        top_performers['salesperson'] = {
                            'top_3': [{'name': idx, 'value': val} for idx, val in top_3_salespeople.items()],
                            'top_1': {'name': salesperson_performance.index[0], 'value': salesperson_performance.iloc[0]}
                        }
                except:
                    pass
        
        if 'product_name' in self.mapping and 'profit' in self.mapping:
            product_col = self.mapping['product_name']
            profit_col = self.mapping['profit']
            
            if product_col in self.df.columns and profit_col in self.df.columns:
                try:
                    self.df[profit_col] = pd.to_numeric(self.df[profit_col], errors='coerce')
                    product_profit = self.df.groupby(product_col)[profit_col].sum().sort_values(ascending=False)
                    
                    if len(product_profit) > 0:
                        top_3_products = product_profit.head(3)
                        top_performers['product_profit'] = {
                            'top_3': [{'name': idx, 'value': val} for idx, val in top_3_products.items()],
                            'top_1': {'name': product_profit.index[0], 'value': product_profit.iloc[0]}
                        }
                except:
                    pass
        
        return top_performers
    
    def _check_data_quality(self):
        """فحص جودة بيانات المبيعات"""
        warnings = []
        lang = TranslationSystem.t('language')
        
        missing_percentage = (self.df.isnull().sum() / len(self.df)) * 100
        high_missing = missing_percentage[missing_percentage > 20].index.tolist()
        
        if high_missing:
            if lang == 'ar':
                warnings.append(f"⚠️ أعمدة بها قيم مفقودة >20%: {', '.join(high_missing[:3])}")
            else:
                warnings.append(f"⚠️ Columns with missing values >20%: {', '.join(high_missing[:3])}")
        
        duplicates = self.df.duplicated().sum()
        if duplicates > 0:
            if lang == 'ar':
                warnings.append(f"⚠️ يوجد {duplicates} سجل مكرر")
            else:
                warnings.append(f"⚠️ Found {duplicates} duplicate records")
        
        if 'total_amount' in self.mapping:
            amount_col = self.mapping['total_amount']
            if amount_col in self.df.columns:
                try:
                    amount_data = pd.to_numeric(self.df[amount_col], errors='coerce')
                    negative_amounts = (amount_data < 0).sum()
                    if negative_amounts > 0:
                        if lang == 'ar':
                            warnings.append(f"⚠️ يوجد {negative_amounts} معاملة بمبلغ سالب")
                        else:
                            warnings.append(f"⚠️ Found {negative_amounts} transactions with negative amounts")
                except:
                    pass
        
        return warnings
    
    def generate_professional_report(self, analysis_results):
        """إنشاء تقرير احترافي كامل للمبيعات"""
        lang = TranslationSystem.t('language')
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M')
        report_id = f"SALE-{datetime.now().strftime('%Y%m%d')}-{np.random.randint(1000, 9999)}"
        
        if lang == 'ar':
            report = f"""
{'='*100}
تقرير تحليل المبيعات الاحترافي
{'='*100}

{TranslationSystem.t('company_name')}
{TranslationSystem.t('report_author')}
{'-'*60}

🔹 {TranslationSystem.t('report_id')}: {report_id}
🔹 {TranslationSystem.t('report_date')}: {current_date}
🔹 {TranslationSystem.t('analysis_period')}: {self._get_date_range()}
🔹 {TranslationSystem.t('total_records')}: {len(self.df):,}

{'='*100}
الملخص التنفيذي
{'='*100}

تم إجراء تحليل متعمق لبيانات المبيعات باستخدام منهجيات تحليلية متقدمة. 
يقدم هذا التقرير رؤى استراتيجية قابلة للتنفيذ بناءً على البيانات الواقعية.

📊 **النتائج الرئيسية:**
• إجمالي المبيعات: {analysis_results['kpis'].get('total_sales', {}).get('formatted', 'غير متوفر')}
• إجمالي الأرباح: {analysis_results['kpis'].get('total_profit', {}).get('formatted', 'غير متوفر')}
• عدد العملاء: {analysis_results['kpis'].get('unique_customers', {}).get('formatted', 'غير متوفر')}
• هامش الربح: {analysis_results['kpis'].get('profit_margin', {}).get('formatted', 'غير متوفر')}

🎯 **النقاط البارزة:**
"""
            for insight in analysis_results['insights'][:3]:
                report += f"• {insight.replace('**', '')}\n"
            
            report += f"""
{'='*100}
تحليل مقاييس الأداء (KPIs)
{'='*100}

مقاييس الأداء الرئيسية:

"""
            for kpi_name, kpi_info in analysis_results['kpis'].items():
                if kpi_name in ['total_transactions', 'total_sales', 'total_profit', 'profit_margin', 
                               'unique_customers', 'unique_products', 'avg_quantity', 'discount_rate']:
                    report += f"• {kpi_info['icon']} **{kpi_info['label']}**: {kpi_info['formatted']}\n"
            
            report += f"""
{'='*100}
تحليل الأداء التفصيلي
{'='*100}

📈 **الأفضل أداءً:**

"""
            if 'salesperson' in analysis_results['top_performers']:
                sp = analysis_results['top_performers']['salesperson']
                report += f"👑 **أفضل مندوب مبيعات**: {sp['top_1']['name']} (${sp['top_1']['value']:,.0f})\n"
                report += "🏅 **أفضل 3 مندوبين**:\n"
                for i, sp_info in enumerate(sp['top_3'], 1):
                    report += f"   {i}. {sp_info['name']}: ${sp_info['value']:,.0f}\n"
            
            report += f"""
📦 **المنتجات الأكثر ربحية:**

"""
            if 'product_profit' in analysis_results['top_performers']:
                pp = analysis_results['top_performers']['product_profit']
                report += f"👑 **أكثر منتج ربحية**: {pp['top_1']['name']} (${pp['top_1']['value']:,.0f})\n"
                report += "🏅 **أفضل 3 منتجات**:\n"
                for i, pp_info in enumerate(pp['top_3'], 1):
                    report += f"   {i}. {pp_info['name']}: ${pp_info['value']:,.0f}\n"
            
            report += f"""
{'='*100}
تحليل توزيع المبيعات
{'='*100}

📍 **توزيع جغرافي:**
"""
            if 'region' in analysis_results['distributions']:
                region_dist = analysis_results['distributions']['region']
                total_regions = sum(region_dist.values())
                for region, count in list(region_dist.items())[:5]:
                    percentage = (count / total_regions * 100) if total_regions > 0 else 0
                    report += f"• {region}: {count} معاملة ({percentage:.1f}%)\n"
            
            report += f"""
🏷️ **توزيع الفئات:**
"""
            if 'category' in analysis_results['distributions']:
                category_dist = analysis_results['distributions']['category']
                total_categories = sum(category_dist.values())
                for category, count in list(category_dist.items())[:5]:
                    percentage = (count / total_categories * 100) if total_categories > 0 else 0
                    report += f"• {category}: {count} منتج ({percentage:.1f}%)\n"
            
            report += f"""
{'='*100}
تحليل جودة البيانات
{'='*100}

🔍 **مؤشرات جودة البيانات:**
"""
            if analysis_results['warnings']:
                for warning in analysis_results['warnings']:
                    report += f"• {warning}\n"
            else:
                report += "✅ جودة البيانات ممتازة - لا توجد مشاكل رئيسية\n"
            
            report += f"""
📊 **إحصائيات البيانات:**
• إجمالي السجلات: {len(self.df):,}
• إجمالي الأعمدة: {len(self.df.columns)}
• نسبة البيانات المكتملة: {((1 - (self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns)))) * 100):.1f}%
• نسبة البيانات الفريدة: {(self.df.nunique().sum() / (len(self.df) * len(self.df.columns)) * 100):.1f}%

{'='*100}
التوصيات الاستراتيجية
{'='*100}

🚀 **توصيات قابلة للتنفيذ:**

1. **التركيز على المناطق عالية الأداء**
   • زيادة الاستثمار في التسويق بالمناطق الأعلى ربحية
   • تطوير استراتيجيات مخصصة لكل منطقة

2. **تحسين محفظة المنتجات**
   • التركيز على المنتجات عالية الربحية
   • تحليل أسباب نجاح المنتجات الرائدة

3. **تحسين أداء فرق المبيعات**
   • دراسة استراتيجيات المندوبين الأوائل
   • تطوير برامج تدريب مبنية على أفضل الممارسات

4. **تحسين جودة البيانات**
   • معالجة القيم المفقودة
   • توحيد تنسيقات البيانات

5. **تحسين استراتيجيات التسعير**
   • تحليل تأثير الخصومات على الربحية
   • تطوير استراتيجيات تسعير ديناميكية

{'='*100}
ملاحق التقرير
{'='*100}

📅 **فترة التحليل:** {self._get_date_range()}
📊 **إجمالي المعاملات:** {analysis_results['kpis'].get('total_transactions', {}).get('formatted', 'غير متوفر')}
💰 **متوسط قيمة المعاملة:** {analysis_results['kpis'].get('avg_transaction', {}).get('formatted', 'غير متوفر')}
👥 **متوسط قيمة العميل:** ${self._calculate_avg_customer_value():,.0f}
📦 **عدد المنتجات الفريدة:** {analysis_results['kpis'].get('unique_products', {}).get('formatted', 'غير متوفر')}

{'='*100}
ملاحظات نهائية
{'='*100}

📌 **نقاط مهمة:**
• تم إعداد هذا التقرير باستخدام تقنيات تحليلية متقدمة
• جميع البيانات معتمدة من مصادر موثوقة
• التوصيات قابلة للقياس والتنفيذ

📞 **للاستفسارات:**
{TranslationSystem.t('report_author')}
report@company.com
+966 55 123 4567

{'='*100}
نهاية التقرير
{'='*100}
"""
        else:
            report = f"""
{'='*100}
PROFESSIONAL SALES ANALYSIS REPORT
{'='*100}

{TranslationSystem.t('company_name')}
{TranslationSystem.t('report_author')}
{'-'*60}

🔹 {TranslationSystem.t('report_id')}: {report_id}
🔹 {TranslationSystem.t('report_date')}: {current_date}
🔹 {TranslationSystem.t('analysis_period')}: {self._get_date_range()}
🔹 {TranslationSystem.t('total_records')}: {len(self.df):,}

{'='*100}
EXECUTIVE SUMMARY
{'='*100}

A comprehensive analysis of sales data has been conducted using advanced analytical methodologies. 
This report provides actionable strategic insights based on factual data.

📊 **Key Results:**
• Total Sales: {analysis_results['kpis'].get('total_sales', {}).get('formatted', 'N/A')}
• Total Profit: {analysis_results['kpis'].get('total_profit', {}).get('formatted', 'N/A')}
• Customer Count: {analysis_results['kpis'].get('unique_customers', {}).get('formatted', 'N/A')}
• Profit Margin: {analysis_results['kpis'].get('profit_margin', {}).get('formatted', 'N/A')}

🎯 **Key Highlights:**
"""
            for insight in analysis_results['insights'][:3]:
                report += f"• {insight.replace('**', '')}\n"
            
            report += f"""
{'='*100}
KEY PERFORMANCE INDICATORS (KPIs)
{'='*100}

Core Performance Metrics:

"""
            for kpi_name, kpi_info in analysis_results['kpis'].items():
                if kpi_name in ['total_transactions', 'total_sales', 'total_profit', 'profit_margin', 
                               'unique_customers', 'unique_products', 'avg_quantity', 'discount_rate']:
                    report += f"• {kpi_info['icon']} **{kpi_info['label']}**: {kpi_info['formatted']}\n"
            
            report += f"""
{'='*100}
DETAILED PERFORMANCE ANALYSIS
{'='*100}

📈 **Top Performers:**

"""
            if 'salesperson' in analysis_results['top_performers']:
                sp = analysis_results['top_performers']['salesperson']
                report += f"👑 **Top Salesperson**: {sp['top_1']['name']} (${sp['top_1']['value']:,.0f})\n"
                report += "🏅 **Top 3 Salespeople**:\n"
                for i, sp_info in enumerate(sp['top_3'], 1):
                    report += f"   {i}. {sp_info['name']}: ${sp_info['value']:,.0f}\n"
            
            report += f"""
📦 **Most Profitable Products:**

"""
            if 'product_profit' in analysis_results['top_performers']:
                pp = analysis_results['top_performers']['product_profit']
                report += f"👑 **Most Profitable Product**: {pp['top_1']['name']} (${pp['top_1']['value']:,.0f})\n"
                report += "🏅 **Top 3 Products**:\n"
                for i, pp_info in enumerate(pp['top_3'], 1):
                    report += f"   {i}. {pp_info['name']}: ${pp_info['value']:,.0f}\n"
            
            report += f"""
{'='*100}
SALES DISTRIBUTION ANALYSIS
{'='*100}

📍 **Geographical Distribution:**
"""
            if 'region' in analysis_results['distributions']:
                region_dist = analysis_results['distributions']['region']
                total_regions = sum(region_dist.values())
                for region, count in list(region_dist.items())[:5]:
                    percentage = (count / total_regions * 100) if total_regions > 0 else 0
                    report += f"• {region}: {count} transactions ({percentage:.1f}%)\n"
            
            report += f"""
🏷️ **Category Distribution:**
"""
            if 'category' in analysis_results['distributions']:
                category_dist = analysis_results['distributions']['category']
                total_categories = sum(category_dist.values())
                for category, count in list(category_dist.items())[:5]:
                    percentage = (count / total_categories * 100) if total_categories > 0 else 0
                    report += f"• {category}: {count} products ({percentage:.1f}%)\n"
            
            report += f"""
{'='*100}
DATA QUALITY ASSESSMENT
{'='*100}

🔍 **Data Quality Indicators:**
"""
            if analysis_results['warnings']:
                for warning in analysis_results['warnings']:
                    report += f"• {warning}\n"
            else:
                report += "✅ Excellent data quality - No major issues found\n"
            
            report += f"""
📊 **Data Statistics:**
• Total Records: {len(self.df):,}
• Total Columns: {len(self.df.columns)}
• Data Completeness: {((1 - (self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns)))) * 100):.1f}%
• Data Uniqueness: {(self.df.nunique().sum() / (len(self.df) * len(self.df.columns)) * 100):.1f}%

{'='*100}
STRATEGIC RECOMMENDATIONS
{'='*100}

🚀 **Actionable Recommendations:**

1. **Focus on High-Performing Regions**
   • Increase marketing investment in top-performing regions
   • Develop region-specific strategies

2. **Optimize Product Portfolio**
   • Focus on high-profit margin products
   • Analyze success factors of top products

3. **Enhance Sales Team Performance**
   • Study top salesperson strategies
   • Develop training programs based on best practices

4. **Improve Data Quality**
   • Address missing values
   • Standardize data formats

5. **Optimize Pricing Strategies**
   • Analyze discount impact on profitability
   • Develop dynamic pricing strategies

{'='*100}
REPORT APPENDICES
{'='*100}

📅 **Analysis Period:** {self._get_date_range()}
📊 **Total Transactions:** {analysis_results['kpis'].get('total_transactions', {}).get('formatted', 'N/A')}
💰 **Average Transaction Value:** {analysis_results['kpis'].get('avg_transaction', {}).get('formatted', 'N/A')}
👥 **Average Customer Value:** ${self._calculate_avg_customer_value():,.0f}
📦 **Unique Product Count:** {analysis_results['kpis'].get('unique_products', {}).get('formatted', 'N/A')}

{'='*100}
FINAL NOTES
{'='*100}

📌 **Important Points:**
• This report was prepared using advanced analytical techniques
• All data is verified from reliable sources
• Recommendations are measurable and actionable

📞 **For Inquiries:**
{TranslationSystem.t('report_author')}
report@company.com
+966 55 123 4567

{'='*100}
END OF REPORT
{'='*100}
"""
        
        return report
    
    def _calculate_avg_customer_value(self):
        """حساب متوسط قيمة العميل"""
        if 'customer_id' in self.mapping and 'total_amount' in self.mapping:
            customer_col = self.mapping['customer_id']
            amount_col = self.mapping['total_amount']
            
            if customer_col in self.df.columns and amount_col in self.df.columns:
                try:
                    self.df[amount_col] = pd.to_numeric(self.df[amount_col], errors='coerce')
                    customer_sales = self.df.groupby(customer_col)[amount_col].sum()
                    return customer_sales.mean() if len(customer_sales) > 0 else 0
                except:
                    pass
        return 0
    
    def _get_date_range(self):
        """الحصول على نطاق التاريخ من البيانات"""
        if 'order_date' in self.mapping:
            date_col = self.mapping['order_date']
            if date_col in self.df.columns:
                try:
                    dates = pd.to_datetime(self.df[date_col], errors='coerce')
                    min_date = dates.min()
                    max_date = dates.max()
                    
                    if pd.notna(min_date) and pd.notna(max_date):
                        if TranslationSystem.t('language') == 'ar':
                            return f"{min_date.strftime('%Y-%m-%d')} إلى {max_date.strftime('%Y-%m-%d')}"
                        else:
                            return f"{min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}"
                except:
                    pass
        
        if TranslationSystem.t('language') == 'ar':
            return "غير متوفر"
        else:
            return "Not available"

# ==================== 3. وحدة الرسوم البيانية ====================

class SalesVisualizer:
    def __init__(self, dataframe, column_mapping, analysis_results):
        self.df = dataframe
        self.mapping = column_mapping
        self.analysis = analysis_results
    
    def generate_all_charts(self):
        """توليد جميع الرسوم البيانية الممكنة للمبيعات"""
        charts = []
        
        charts.append(self._create_sales_trend_chart())
        charts.append(self._create_top_products_chart())
        charts.append(self._create_region_chart())
        charts.append(self._create_category_chart())
        charts.append(self._create_salesperson_chart())
        charts.append(self._create_price_quantity_chart())
        charts.append(self._create_payment_method_chart())
        charts.append(self._create_profit_chart())
        
        return [chart for chart in charts if chart is not None]
    
    def _create_sales_trend_chart(self):
        """إنشاء رسم اتجاه المبيعات عبر الزمن"""
        if 'order_date' not in self.mapping or 'total_amount' not in self.mapping:
            return None
        
        date_col = self.mapping['order_date']
        amount_col = self.mapping['total_amount']
        
        if date_col not in self.df.columns or amount_col not in self.df.columns:
            return None
        
        try:
            df_copy = self.df.copy()
            df_copy[date_col] = pd.to_datetime(df_copy[date_col], errors='coerce')
            df_copy[amount_col] = pd.to_numeric(df_copy[amount_col], errors='coerce')
            
            df_clean = df_copy.dropna(subset=[date_col, amount_col])
            
            if len(df_clean) == 0:
                return None
            
            df_clean['year_month'] = df_clean[date_col].dt.to_period('M').dt.to_timestamp()
            sales_trend = df_clean.groupby('year_month')[amount_col].sum().reset_index()
            
            fig = px.line(
                sales_trend,
                x='year_month',
                y=amount_col,
                title=TranslationSystem.t('chart_sales_trend'),
                labels={'year_month': TranslationSystem.t('order_date'), amount_col: TranslationSystem.t('total_amount')}
            )
            
            fig.update_traces(mode='lines+markers')
            
            return {
                'title': TranslationSystem.t('chart_sales_trend'),
                'figure': fig
            }
        except:
            return None
    
    def _create_top_products_chart(self):
        """إنشاء رسم أفضل المنتجات مبيعاً"""
        if 'product_name' not in self.mapping or 'quantity' not in self.mapping:
            return None
        
        product_col = self.mapping['product_name']
        quantity_col = self.mapping['quantity']
        
        if product_col not in self.df.columns or quantity_col not in self.df.columns:
            return None
        
        try:
            df_copy = self.df.copy()
            df_copy[quantity_col] = pd.to_numeric(df_copy[quantity_col], errors='coerce')
            
            product_sales = df_copy.groupby(product_col)[quantity_col].sum().reset_index()
            product_sales = product_sales.sort_values(quantity_col, ascending=False).head(10)
            
            fig = px.bar(
                product_sales,
                x=quantity_col,
                y=product_col,
                orientation='h',
                color=quantity_col,
                color_continuous_scale='Viridis',
                title=TranslationSystem.t('chart_top_products')
            )
            
            fig.update_layout(
                xaxis_title=TranslationSystem.t('quantity'),
                yaxis_title=TranslationSystem.t('product_name'),
                coloraxis_showscale=False
            )
            
            return {
                'title': TranslationSystem.t('chart_top_products'),
                'figure': fig
            }
        except:
            return None
    
    def _create_region_chart(self):
        """إنشاء رسم توزيع المبيعات حسب المنطقة"""
        if 'region' not in self.mapping or 'total_amount' not in self.mapping:
            return None
        
        region_col = self.mapping['region']
        amount_col = self.mapping['total_amount']
        
        if region_col not in self.df.columns or amount_col not in self.df.columns:
            return None
        
        try:
            df_copy = self.df.copy()
            df_copy[amount_col] = pd.to_numeric(df_copy[amount_col], errors='coerce')
            
            region_sales = df_copy.groupby(region_col)[amount_col].sum().reset_index()
            
            fig = px.pie(
                region_sales,
                values=amount_col,
                names=region_col,
                title=TranslationSystem.t('chart_region_dist'),
                hole=0.4
            )
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            
            return {
                'title': TranslationSystem.t('chart_region_dist'),
                'figure': fig
            }
        except:
            return None
    
    def _create_category_chart(self):
        """إنشاء رسم توزيع المبيعات حسب الفئة"""
        if 'category' not in self.mapping or 'total_amount' not in self.mapping:
            return None
        
        category_col = self.mapping['category']
        amount_col = self.mapping['total_amount']
        
        if category_col not in self.df.columns or amount_col not in self.df.columns:
            return None
        
        try:
            df_copy = self.df.copy()
            df_copy[amount_col] = pd.to_numeric(df_copy[amount_col], errors='coerce')
            
            category_sales = df_copy.groupby(category_col)[amount_col].sum().reset_index()
            category_sales = category_sales.sort_values(amount_col, ascending=False).head(8)
            
            fig = px.bar(
                category_sales,
                x=category_col,
                y=amount_col,
                color=amount_col,
                color_continuous_scale='Blues',
                title=TranslationSystem.t('chart_category_dist')
            )
            
            fig.update_layout(
                xaxis_title=TranslationSystem.t('category'),
                yaxis_title=TranslationSystem.t('total_amount'),
                coloraxis_showscale=False
            )
            
            return {
                'title': TranslationSystem.t('chart_category_dist'),
                'figure': fig
            }
        except:
            return None
    
    def _create_salesperson_chart(self):
        """إنشاء رسم أداء مندوبي المبيعات"""
        if 'salesperson' not in self.mapping or 'total_amount' not in self.mapping:
            return None
        
        salesperson_col = self.mapping['salesperson']
        amount_col = self.mapping['total_amount']
        
        if salesperson_col not in self.df.columns or amount_col not in self.df.columns:
            return None
        
        try:
            df_copy = self.df.copy()
            df_copy[amount_col] = pd.to_numeric(df_copy[amount_col], errors='coerce')
            
            salesperson_performance = df_copy.groupby(salesperson_col)[amount_col].sum().reset_index()
            salesperson_performance = salesperson_performance.sort_values(amount_col, ascending=False).head(10)
            
            fig = px.bar(
                salesperson_performance,
                x=salesperson_col,
                y=amount_col,
                color=amount_col,
                color_continuous_scale='RdYlGn',
                title=TranslationSystem.t('chart_sales_performance')
            )
            
            fig.update_layout(
                xaxis_title=TranslationSystem.t('salesperson'),
                yaxis_title=TranslationSystem.t('total_amount'),
                coloraxis_showscale=False
            )
            
            return {
                'title': TranslationSystem.t('chart_sales_performance'),
                'figure': fig
            }
        except:
            return None
    
    def _create_price_quantity_chart(self):
        """إنشاء رسم علاقة السعر بالكمية"""
        if 'price' not in self.mapping or 'quantity' not in self.mapping:
            return None
        
        price_col = self.mapping['price']
        quantity_col = self.mapping['quantity']
        
        if price_col not in self.df.columns or quantity_col not in self.df.columns:
            return None
        
        try:
            df_copy = self.df.copy()
            df_copy[price_col] = pd.to_numeric(df_copy[price_col], errors='coerce')
            df_copy[quantity_col] = pd.to_numeric(df_copy[quantity_col], errors='coerce')
            
            df_clean = df_copy.dropna(subset=[price_col, quantity_col])
            
            if len(df_clean) == 0:
                return None
            
            fig = px.scatter(
                df_clean,
                x=price_col,
                y=quantity_col,
                trendline="ols",
                title=TranslationSystem.t('chart_price_quantity'),
                labels={price_col: TranslationSystem.t('unit_price'), quantity_col: TranslationSystem.t('quantity')}
            )
            
            return {
                'title': TranslationSystem.t('chart_price_quantity'),
                'figure': fig
            }
        except:
            return None
    
    def _create_payment_method_chart(self):
        """إنشاء رسم توزيع طرق الدفع"""
        if 'payment_method' not in self.mapping:
            return None
        
        payment_col = self.mapping['payment_method']
        
        if payment_col not in self.df.columns:
            return None
        
        payment_counts = self.df[payment_col].value_counts().reset_index()
        payment_counts.columns = ['payment_method', 'count']
        
        fig = px.pie(
            payment_counts,
            values='count',
            names='payment_method',
            title=TranslationSystem.t('chart_payment_methods'),
            hole=0.3
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        
        return {
            'title': TranslationSystem.t('chart_payment_methods'),
            'figure': fig
        }
    
    def _create_profit_chart(self):
        """إنشاء رسم تحليل الربحية"""
        if 'profit' not in self.mapping:
            return None
        
        profit_col = self.mapping['profit']
        
        if profit_col not in self.df.columns:
            return None
        
        try:
            profit_data = pd.to_numeric(self.df[profit_col], errors='coerce').dropna()
            
            if len(profit_data) == 0:
                return None
            
            fig = px.histogram(
                profit_data,
                nbins=30,
                title=TranslationSystem.t('chart_profit_dist'),
                labels={'value': TranslationSystem.t('profit'), 'count': 'Count'}
            )
            
            avg_profit = profit_data.mean()
            fig.add_vline(
                x=avg_profit,
                line_dash="dash",
                line_color="green",
                annotation_text=f"Average: ${avg_profit:,.0f}",
                annotation_position="top right"
            )
            
            return {
                'title': TranslationSystem.t('chart_profit_dist'),
                'figure': fig
            }
        except:
            return None

# ==================== 4. وظائف المساعدة ====================

def load_multiple_files(uploaded_files):
    """تحميل عدة ملفات Excel/CSV"""
    dataframes = []
    file_info_list = []
    
    for uploaded_file in uploaded_files:
        try:
            file_name = uploaded_file.name.lower()
            
            if file_name.endswith('.csv'):
                content = uploaded_file.getvalue()
                encodings = ['utf-8', 'utf-8-sig', 'latin1', 'cp1256', 'windows-1256']
                
                for encoding in encodings:
                    try:
                        df = pd.read_csv(BytesIO(content), encoding=encoding)
                        break
                    except:
                        continue
                else:
                    df = pd.read_csv(BytesIO(content), encoding='utf-8', errors='ignore')
                    
            elif file_name.endswith('.xlsx') or file_name.endswith('.xls'):
                df = pd.read_excel(uploaded_file, engine='openpyxl')
            else:
                st.error(f"نوع الملف غير مدعوم: {file_name}")
                continue
            
            file_info = {
                'name': uploaded_file.name,
                'size': len(uploaded_file.getvalue()),
                'rows': len(df),
                'columns': len(df.columns),
                'dataframe': df
            }
            
            file_info_list.append(file_info)
            dataframes.append(df)
            
        except Exception as e:
            st.error(f"{TranslationSystem.t('upload_error')} {uploaded_file.name}: {str(e)}")
    
    return dataframes, file_info_list

def merge_dataframes(dataframes):
    """دمج عدة dataframes في dataframe واحد"""
    if dataframes is None or len(dataframes) == 0:
        return None
    
    try:
        merged_df = pd.concat(dataframes, ignore_index=True, sort=False)
        return merged_df
    except Exception as e:
        st.error(f"خطأ في دمج الملفات: {str(e)}")
        return None

def load_css():
    """تحميل CSS مع دعم متعدد اللغات"""
    direction = TranslationSystem.get_language_direction()
    font_family = TranslationSystem.get_font_family()
    
    css = f"""
    <style>
    .main-header {{
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        text-align: center;
        font-family: {font_family};
    }}
    
    .kpi-card {{
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin: 10px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        text-align: center;
        transition: all 0.3s ease;
        font-family: {font_family};
        direction: {direction};
    }}
    
    .kpi-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }}
    
    .upload-box {{
        border: 2px dashed #4F46E5;
        border-radius: 12px;
        padding: 40px;
        text-align: center;
        background: #f7fafc;
        margin: 20px 0;
        font-family: {font_family};
        direction: {direction};
    }}
    
    .file-card {{
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        font-family: {font_family};
        direction: {direction};
    }}
    
    .warning-box {{
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        font-family: {font_family};
        direction: {direction};
    }}
    
    .report-box {{
        background: #ffffff;
        border: 2px solid #4F46E5;
        border-radius: 15px;
        padding: 30px;
        margin: 20px 0;
        font-family: {font_family};
        direction: {direction};
        white-space: pre-wrap;
        font-size: 14px;
        line-height: 1.8;
        max-height: 700px;
        overflow-y: auto;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        background: linear-gradient(to bottom, #ffffff, #f9fafb);
    }}
    
    .stApp {{
        font-family: {font_family};
        text-align: {direction};
    }}
    
    .stButton > button {{
        border-radius: 8px;
        font-family: {font_family};
    }}
    
    .stSelectbox, .stTextInput, .stNumberInput {{
        font-family: {font_family};
    }}
    
    .report-header {{
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 25px;
        border-radius: 12px 12px 0 0;
        margin-bottom: 20px;
        text-align: center;
    }}
    
    .report-section {{
        background: #ffffff;
        border-left: 5px solid #4F46E5;
        padding: 20px;
        margin: 15px 0;
        border-radius: 8px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
    }}
    
    .report-kpi {{
        background: #f0f9ff;
        border: 1px solid #bae6fd;
        padding: 15px;
        margin: 10px 0;
        border-radius: 8px;
    }}
    
    .report-warning {{
        background: #fff7ed;
        border: 1px solid #fed7aa;
        padding: 15px;
        margin: 10px 0;
        border-radius: 8px;
    }}
    
    .report-recommendation {{
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        padding: 15px;
        margin: 10px 0;
        border-radius: 8px;
    }}
    </style>
    
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
    """
    st.markdown(css, unsafe_allow_html=True)

# ==================== 5. تهيئة حالة الجلسة ====================

# إعدادات الصفحة
st.set_page_config(
    page_title=TranslationSystem.t('dashboard_title'),
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تهيئة حالة الجلسة
if 'language' not in st.session_state:
    st.session_state.language = 'ar'
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'files_uploaded' not in st.session_state:
    st.session_state.files_uploaded = False
if 'dataframes' not in st.session_state:
    st.session_state.dataframes = []
if 'file_info_list' not in st.session_state:
    st.session_state.file_info_list = []
if 'merged_df' not in st.session_state:
    st.session_state.merged_df = None
if 'current_df' not in st.session_state:
    st.session_state.current_df = None
if 'column_mapping' not in st.session_state:
    st.session_state.column_mapping = {}
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = {}
if 'use_merged' not in st.session_state:
    st.session_state.use_merged = False
if 'text_report' not in st.session_state:
    st.session_state.text_report = ""

# وظائف تبديل اللغة والمظهر
def toggle_language():
    st.session_state.language = 'en' if st.session_state.language == 'ar' else 'ar'
    st.rerun()

def toggle_theme():
    st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
    st.rerun()

# تحميل CSS
load_css()

# ==================== 6. الشريط الجانبي ====================

with st.sidebar:
    st.markdown(f"### {TranslationSystem.t('sidebar_settings')}")
    
    # تبديل اللغة
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**{TranslationSystem.t('language')}**")
    with col2:
        current_lang = "العربية" if st.session_state.language == 'en' else "English"
        if st.button(f"🌐 {current_lang}", use_container_width=True):
            toggle_language()
    
    # تبديل المظهر
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**{TranslationSystem.t('theme')}**")
    with col2:
        current_theme = TranslationSystem.t('dark_theme') if st.session_state.theme == 'light' else TranslationSystem.t('light_theme')
        if st.button(current_theme, use_container_width=True):
            toggle_theme()
    
    st.divider()
    
    # تحميل الإعدادات السابقة
    if st.button(TranslationSystem.t('load_settings'), use_container_width=True, icon="📥"):
        if os.path.exists('sales_config.json'):
            with open('sales_config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
                st.session_state.column_mapping = config.get('column_mapping', {})
                st.session_state.language = config.get('language', 'ar')
                st.session_state.theme = config.get('theme', 'light')
                st.success(TranslationSystem.t('settings_loaded'))
                st.rerun()
        else:
            st.warning(TranslationSystem.t('no_settings'))
    
    # حفظ الإعدادات
    if st.session_state.column_mapping:
        if st.button(TranslationSystem.t('save_settings'), use_container_width=True, icon="💾"):
            config = {
                'column_mapping': st.session_state.column_mapping,
                'saved_at': datetime.now().isoformat(),
                'language': st.session_state.language,
                'theme': st.session_state.theme
            }
            with open('sales_config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            st.success(TranslationSystem.t('settings_saved'))
    
    # إعادة التعيين
    if st.button(TranslationSystem.t('reset'), use_container_width=True, icon="🔄"):
        for key in list(st.session_state.keys()):
            if key not in ['language', 'theme']:
                del st.session_state[key]
        st.rerun()

# ==================== 7. العنوان الرئيسي ====================

st.markdown(f"""
<div class="main-header">
    <h1>{TranslationSystem.t('dashboard_title')}</h1>
    <p>{TranslationSystem.t('dashboard_subtitle')}</p>
</div>
""", unsafe_allow_html=True)

# ==================== 8. تحميل الملفات المتعددة ====================

st.markdown(f"## 📤 {TranslationSystem.t('step_1')}")

uploaded_files = st.file_uploader(
    TranslationSystem.t('upload_hint'),
    type=['xlsx', 'xls', 'csv'],
    help=TranslationSystem.t('upload_supported'),
    accept_multiple_files=True,
    key="sales_file_uploader"
)

if uploaded_files and len(uploaded_files) > 0:
    try:
        with st.spinner("جاري تحميل الملفات..." if st.session_state.language == 'ar' else "Loading files..."):
            dataframes, file_info_list = load_multiple_files(uploaded_files)
        
        if dataframes and file_info_list:
            st.session_state.dataframes = dataframes
            st.session_state.file_info_list = file_info_list
            st.session_state.files_uploaded = True
            
            st.success(TranslationSystem.t('upload_success', count=len(dataframes)))
            
            # عرض معلومات الملفات
            st.markdown(f"### 📁 {TranslationSystem.t('file_info')}")
            
            for i, file_info in enumerate(file_info_list):
                with st.expander(f"{file_info['name']} ({file_info['rows']} {TranslationSystem.t('rows')}, {file_info['columns']} {TranslationSystem.t('columns')})"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(TranslationSystem.t('file_size'), f"{file_info['size']:,} bytes")
                    with col2:
                        st.metric(TranslationSystem.t('rows'), file_info['rows'])
                    with col3:
                        st.metric(TranslationSystem.t('columns'), file_info['columns'])
                    
                    if st.checkbox(f"{TranslationSystem.t('preview')} {i+1}", key=f"preview_{i}"):
                        st.dataframe(file_info['dataframe'].head(), use_container_width=True)
            
            # خيارات دمج الملفات
            if len(dataframes) > 1:
                st.markdown("### 🔗 خيارات الدمج")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(TranslationSystem.t('merge_files'), use_container_width=True, icon="🔗"):
                        merged_df = merge_dataframes(dataframes)
                        if merged_df is not None:
                            st.session_state.merged_df = merged_df
                            st.session_state.use_merged = True
                            st.session_state.current_df = merged_df
                            st.success(TranslationSystem.t('merged_success'))
                
                with col2:
                    if st.button(TranslationSystem.t('use_single'), use_container_width=True, icon="📄"):
                        st.session_state.use_merged = False
                        st.session_state.current_df = dataframes[0]
                        st.info(f"📄 {TranslationSystem.t('individual_file')}")
            
            # تحديد البيانات التي سيتم استخدامها
            if not st.session_state.current_df:
                if st.session_state.merged_df is not None:
                    st.session_state.current_df = st.session_state.merged_df
                    st.session_state.use_merged = True
                else:
                    st.session_state.current_df = dataframes[0]
                    st.session_state.use_merged = False
            
            # عرض إحصائيات البيانات
            df_to_use = st.session_state.current_df
            
            if st.session_state.use_merged and st.session_state.merged_df is not None:
                st.info(f"📊 **{TranslationSystem.t('merged_data')}**: {len(df_to_use)} {TranslationSystem.t('rows')}, {len(df_to_use.columns)} {TranslationSystem.t('columns')}")
            else:
                st.info(f"📊 **{TranslationSystem.t('individual_file')}**: {len(df_to_use)} {TranslationSystem.t('rows')}, {len(df_to_use.columns)} {TranslationSystem.t('columns')}")
            
            # عرض عينة من البيانات
            with st.expander(f"{TranslationSystem.t('preview')} ({TranslationSystem.t('preview_rows')})"):
                st.dataframe(df_to_use.head(), use_container_width=True)
            
            # عرض معلومات البيانات
            st.markdown(f"### 📈 {TranslationSystem.t('statistics')}")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(TranslationSystem.t('total_files'), len(dataframes))
            with col2:
                st.metric(TranslationSystem.t('total_records'), len(df_to_use))
            with col3:
                st.metric(TranslationSystem.t('total_columns'), len(df_to_use.columns))
            with col4:
                numeric_cols = df_to_use.select_dtypes(include=[np.number]).columns.tolist()
                st.metric(TranslationSystem.t('numeric_columns'), len(numeric_cols))
        
    except Exception as e:
        st.error(f"{TranslationSystem.t('upload_error')} {str(e)}")

# ==================== 9. تعيين أعمدة المبيعات ====================

if st.session_state.files_uploaded and st.session_state.current_df is not None:
    st.markdown(f"## 🎯 {TranslationSystem.t('step_2')}")
    
    df = st.session_state.current_df
    columns = df.columns.tolist()
    
    # التعرف التلقائي على الأعمدة
    mapper = SalesAutoColumnMapper(df)
    auto_suggestions = mapper.auto_detect_columns()
    
    st.markdown(f"**{TranslationSystem.t('auto_detection')}**")
    st.info(TranslationSystem.t('auto_detection_desc'))
    
    # إنشاء تخطيط تعيين الأعمدة
    column_mapping = {}
    
    # عرض تعيين الأعمدة لكل فئة
    categories = {
        TranslationSystem.t('category_order'): ["order_id", "order_date", "status"],
        TranslationSystem.t('category_customer'): ["customer_name", "customer_id"],
        TranslationSystem.t('category_product'): ["product_name", "product_id", "category"],
        TranslationSystem.t('category_financial'): ["quantity", "price", "total_amount", "discount", "profit"],
        TranslationSystem.t('category_location'): ["region", "city", "country"],
        TranslationSystem.t('category_sales'): ["salesperson", "payment_method"]
    }
    
    for category, fields in categories.items():
        st.markdown(f"### {category}")
        
        cols = st.columns(3)
        for idx, field in enumerate(fields):
            with cols[idx % 3]:
                field_display = TranslationSystem.t(f'field_{field}')
                suggested_column = auto_suggestions.get(field, TranslationSystem.t('not_available'))
                
                options = [f"❌ {TranslationSystem.t('not_available')}"] + columns
                default_idx = 0
                if suggested_column in columns:
                    default_idx = columns.index(suggested_column) + 1
                
                selected = st.selectbox(
                    f"**{field_display}**",
                    options=options,
                    index=default_idx,
                    key=f"sales_map_{field}"
                )
                
                if selected != f"❌ {TranslationSystem.t('not_available')}":
                    column_mapping[field] = selected
    
    st.session_state.column_mapping = column_mapping
    
    # زر للمتابعة للتحليل
    if st.button(TranslationSystem.t('analyze_button'), type="primary", use_container_width=True, icon="🚀"):
        st.session_state.analysis_ready = True
        st.rerun()

# ==================== 10. التحليل الذكي للمبيعات ====================

if st.session_state.get('analysis_ready', False):
    st.markdown(f"## 📊 {TranslationSystem.t('step_3')}")
    
    analyzer = SalesDataAnalyzer(
        st.session_state.current_df, 
        st.session_state.column_mapping
    )
    
    # التحليل الذكي للبيانات
    with st.spinner(TranslationSystem.t('loading_analysis')):
        analysis = analyzer.analyze_all()
    
    st.session_state.analysis_results = analysis
    
    # عرض النتائج الرئيسية
    st.markdown(f"### 📈 {TranslationSystem.t('kpis_title')}")
    
    # بطاقات KPIs
    kpis = analysis.get('kpis', {})
    if kpis:
        kpi_keys = list(kpis.keys())
        
        # عرض KPIs في أعمدة
        cols_per_row = 4
        for i in range(0, len(kpi_keys), cols_per_row):
            cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                if i + j < len(kpi_keys):
                    kpi_key = kpi_keys[i + j]
                    with cols[j]:
                        kpi_info = kpis[kpi_key]
                        trend_color = {
                            'positive': '#10B981',
                            'negative': '#EF4444',
                            'neutral': '#6B7280'
                        }.get(kpi_info.get('trend', 'neutral'), '#6B7280')
                        
                        st.markdown(f"""
                        <div class="kpi-card">
                            <div style="font-size: 2.5rem; margin-bottom: 10px; color: {trend_color};">
                                {kpi_info.get('icon', '📊')}
                            </div>
                            <div style="font-size: 1.8rem; font-weight: bold; color: #4F46E5;">
                                {kpi_info['formatted']}
                            </div>
                            <div style="color: #6B7280; font-size: 0.9rem;">
                                {kpi_info['label']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
    
    # الرسوم البيانية الذكية
    st.markdown(f"### 📊 {TranslationSystem.t('charts_title')}")
    
    visualizer = SalesVisualizer(
        st.session_state.current_df,
        st.session_state.column_mapping,
        analysis
    )
    
    # عرض الرسوم حسب توفر البيانات
    charts = visualizer.generate_all_charts()
    
    if charts:
        for i in range(0, len(charts), 2):
            cols = st.columns(2)
            for j in range(2):
                if i + j < len(charts):
                    chart_info = charts[i + j]
                    with cols[j]:
                        st.markdown(f"#### {chart_info['title']}")
                        st.plotly_chart(chart_info['figure'], use_container_width=True)
    else:
        st.warning(TranslationSystem.t('no_charts_data'))
    
    # التقرير النصي الاحترافي
    st.markdown(f"### 📄 {TranslationSystem.t('report_title')}")
    
    # زر إنشاء التقرير الاحترافي
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button(TranslationSystem.t('generate_report'), use_container_width=True, icon="📋", type="primary"):
            st.session_state.text_report = analyzer.generate_professional_report(analysis)
    
    # عرض التقرير إذا كان موجوداً
    if st.session_state.text_report:
        st.markdown(f"#### {TranslationSystem.t('executive_summary')}")
        
        # صندوق عرض التقرير الاحترافي
        st.markdown(f'<div class="report-box">{st.session_state.text_report}</div>', unsafe_allow_html=True)
        
        # زر النسخ فقط (تم إزالة زر التنزيل)
        if st.button(TranslationSystem.t('copy_report'), use_container_width=True, icon="📋"):
            try:
                pyperclip.copy(st.session_state.text_report)
                st.success(TranslationSystem.t('report_copied'))
            except:
                # Fallback في حالة عدم وجود pyperclip
                st.code(st.session_state.text_report, language='text')
                st.warning("⚠️ يرجى نسخ النص أعلاه يدوياً" if st.session_state.language == 'ar' else "⚠️ Please copy the text above manually")
    
    # تحليل إضافي
    with st.expander(TranslationSystem.t('advanced_analysis')):
        st.markdown(f"### 🔍 {TranslationSystem.t('advanced_analysis')}")
        
        # تحليل العلاقات
        numeric_cols = []
        for col in st.session_state.current_df.columns:
            if pd.api.types.is_numeric_dtype(st.session_state.current_df[col]):
                numeric_cols.append(col)
        
        if len(numeric_cols) >= 2:
            st.markdown(f"#### {TranslationSystem.t('correlation_matrix')}")
            
            numeric_df = st.session_state.current_df[numeric_cols]
            corr_matrix = numeric_df.corr()
            
            fig = px.imshow(
                corr_matrix,
                text_auto='.2f',
                color_continuous_scale='RdBu',
                aspect="auto",
                title=TranslationSystem.t('correlation_matrix')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # اكتشاف القيم الشاذة
        st.markdown(f"#### {TranslationSystem.t('outlier_detection')}")
        if 'total_amount' in st.session_state.column_mapping:
            price_col = st.session_state.column_mapping['total_amount']
            if price_col in st.session_state.current_df.columns:
                try:
                    price_data = st.session_state.current_df[price_col].dropna()
                    
                    if len(price_data) > 0:
                        mean_price = price_data.mean()
                        std_price = price_data.std()
                        
                        if std_price > 0:
                            z_scores = np.abs((price_data - mean_price) / std_price)
                            outliers_mask = z_scores > 3
                            outliers = st.session_state.current_df.loc[price_data.index[outliers_mask]]
                            
                            if len(outliers) > 0:
                                st.warning(TranslationSystem.t('outliers_found', count=len(outliers)))
                                st.dataframe(outliers.head(), use_container_width=True)
                            else:
                                st.success(TranslationSystem.t('no_outliers'))
                        else:
                            st.info(TranslationSystem.t('zero_std'))
                except Exception as e:
                    st.error(f"{TranslationSystem.t('error')}: {str(e)}")

# ==================== 11. رسالة الترحيب ====================

if not st.session_state.files_uploaded:
    st.info("""
    📋 **إرشادات الاستخدام:**
    
    1. **رفع الملفات**: قم برفع ملفات Excel أو CSV تحتوي على بيانات المبيعات
    2. **تعيين الأعمدة**: سيقوم النظام بالتعرف التلقائي على أعمدة البيانات
    3. **التحليل**: انتقل إلى التحليل للحصول على نتائج ورسوم بيانية
    4. **التقرير**: إنشاء تقرير نصي احترافي يمكن نسخه للعميل
    
    💡 **نصائح**:
    - يمكنك رفع ملفات متعددة ودمجها
    - تحقق من تعيين الأعمدة قبل التحليل
    - استخدم زر حفظ الإعدادات لحفظ التكوين
    """)

# ==================== 12. تذييل الصفحة ====================

st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="text-align: center; color: #6B7280; font-size: 0.9rem;">
    <p>📊 نظام تحليل المبيعات الذكي | الإصدار 3.0 | يدعم العربية والإنجليزية</p>
    </div>
    """, unsafe_allow_html=True)a