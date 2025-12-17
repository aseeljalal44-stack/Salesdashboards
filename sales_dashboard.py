"""
لوحة تحكم المبيعات الاحترافية - منتج تحليلي متكامل
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

# ==================== 1. نظام الترجمة المتكامل ====================

class TranslationSystem:
    """نظام ترجمة متكامل ثنائي اللغة"""
    
    TRANSLATIONS = {
        'ar': {
            # العنوان الرئيسي
            'dashboard_title': '📊 لوحة تحكم المبيعات الذكية',
            'dashboard_subtitle': 'تحليل احترافي لبيانات المبيعات - مصمم للشركات الصغيرة والمتوسطة',
            'audience_target': 'هذا المنتج مصمم للشركات الصغيرة والمتوسطة لفهم أداء المبيعات بسرعة',
            
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
            'kpi_customers': 'عدد العملاء',
            'kpi_products': 'عدد المنتجات',
            'kpi_avg_quantity': 'متوسط الكمية',
            'kpi_discount_rate': 'معدل الخصم',
            'gross_profit': 'الربح الإجمالي',
            'gross_margin': 'هامش الربح الإجمالي',
            
            # التعريفات
            'def_gross_profit': 'المبلغ المتبقي من الإيرادات بعد خصم تكلفة البضاعة المباعة',
            'def_gross_margin': 'النسبة المئوية للإيرادات المتبقية بعد خصم تكلفة البضاعة المباعة',
            'def_total_sales': 'إجمالي الإيرادات من جميع المعاملات',
            'def_transactions': 'عدد الفواتير أو المعاملات المكتملة',
            
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
            
            # التقرير
            'report_title': '📄 التقرير التحليلي',
            'generate_report': '📋 إنشاء التقرير',
            'copy_report': '📋 نسخ التقرير',
            'report_copied': '✅ تم نسخ التقرير إلى الحافظة',
            'executive_summary': 'الملخص التنفيذي',
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
            'definition': 'تعريف',
            'explanation': 'تفسير',
            
            # تعريفات النقاط
            'missing_values_desc': 'نسبة البيانات الناقصة في هذا العمود',
            'duplicates_desc': 'سجلات متكررة قد تؤثر على دقة التحليل',
            'data_uniqueness_desc': 'تكرر العملاء أو المنتجات - طبيعي في بيانات التجزئة',
        },
        
        'en': {
            # Main Title
            'dashboard_title': '📊 Smart Sales Analytics Dashboard',
            'dashboard_subtitle': 'Professional sales data analysis - Designed for small and medium businesses',
            'audience_target': 'This product is designed for small and medium businesses to quickly understand sales performance',
            
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
            'kpi_customers': 'Number of Customers',
            'kpi_products': 'Number of Products',
            'kpi_avg_quantity': 'Average Quantity',
            'kpi_discount_rate': 'Discount Rate',
            'gross_profit': 'Gross Profit',
            'gross_margin': 'Gross Margin',
            
            # Definitions
            'def_gross_profit': 'Revenue remaining after deducting cost of goods sold',
            'def_gross_margin': 'Percentage of revenue remaining after deducting cost of goods sold',
            'def_total_sales': 'Total revenue from all transactions',
            'def_transactions': 'Number of completed invoices or transactions',
            
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
            
            # Report
            'report_title': '📄 Analytical Report',
            'generate_report': '📋 Generate Report',
            'copy_report': '📋 Copy Report',
            'report_copied': '✅ Report copied to clipboard',
            'executive_summary': 'Executive Summary',
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
            'definition': 'Definition',
            'explanation': 'Explanation',
            
            # Point definitions
            'missing_values_desc': 'Percentage of missing data in this column',
            'duplicates_desc': 'Duplicate records that may affect analysis accuracy',
            'data_uniqueness_desc': 'Repeated customers or products - expected in retail datasets',
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

# ==================== 2. وحدة التحليل الذكي (مُحسنة) ====================

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
        lang = st.session_state.get('language', 'ar')
        
        # إجمالي عدد المعاملات
        total_transactions = len(self.df)
        kpis['total_transactions'] = {
            'value': total_transactions,
            'formatted': f"{total_transactions:,}",
            'label': TranslationSystem.t('kpi_transactions'),
            'icon': '🛒',
            'trend': 'neutral',
            'definition': TranslationSystem.t('def_transactions')
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
                        'trend': 'positive' if total_sales > 0 else 'negative',
                        'definition': TranslationSystem.t('def_total_sales')
                    }
                    
                    avg_transaction = total_sales / total_transactions if total_transactions > 0 else 0
                    kpis['avg_transaction'] = {
                        'value': avg_transaction,
                        'formatted': f"${avg_transaction:,.0f}",
                        'label': TranslationSystem.t('kpi_avg_transaction'),
                        'icon': '📊',
                        'trend': 'positive' if avg_transaction > 0 else 'negative'
                    }
                except Exception as e:
                    st.error(f"خطأ في حساب المبيعات: {str(e)}" if lang == 'ar' else f"Error calculating sales: {str(e)}")
        
        # حساب الربح الإجمالي وهامش الربح الإجمالي
        if 'cost' in self.mapping and 'total_amount' in self.mapping:
            cost_col = self.mapping['cost']
            amount_col = self.mapping['total_amount']
            
            if cost_col in self.df.columns and amount_col in self.df.columns:
                try:
                    self.df[cost_col] = pd.to_numeric(self.df[cost_col], errors='coerce')
                    self.df[amount_col] = pd.to_numeric(self.df[amount_col], errors='coerce')
                    
                    # حساب تكلفة البضاعة المباعة
                    if 'quantity' in self.mapping:
                        quantity_col = self.mapping['quantity']
                        if quantity_col in self.df.columns:
                            self.df[quantity_col] = pd.to_numeric(self.df[quantity_col], errors='coerce')
                            total_cogs = (self.df[cost_col] * self.df[quantity_col]).sum()
                        else:
                            total_cogs = self.df[cost_col].sum()
                    else:
                        total_cogs = self.df[cost_col].sum()
                    
                    total_sales = self.df[amount_col].sum()
                    gross_profit = total_sales - total_cogs
                    gross_margin = (gross_profit / total_sales * 100) if total_sales > 0 else 0
                    
                    kpis['gross_profit'] = {
                        'value': gross_profit,
                        'formatted': f"${gross_profit:,.0f}",
                        'label': TranslationSystem.t('gross_profit'),
                        'icon': '📈',
                        'trend': 'positive' if gross_profit > 0 else 'negative',
                        'definition': TranslationSystem.t('def_gross_profit')
                    }
                    
                    kpis['gross_margin'] = {
                        'value': gross_margin,
                        'formatted': f"{gross_margin:.1f}%",
                        'label': TranslationSystem.t('gross_margin'),
                        'icon': '📊',
                        'trend': 'positive' if gross_margin > 15 else 'neutral',
                        'definition': TranslationSystem.t('def_gross_margin')
                    }
                except Exception as e:
                    if lang == 'ar':
                        st.warning("لم يتم حساب الربح بسبب مشكلة في البيانات")
                    else:
                        st.warning("Profit calculation skipped due to data issue")
        
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
    
    def _check_data_quality(self):
        """فحص جودة بيانات المبيعات"""
        warnings = []
        lang = st.session_state.get('language', 'ar')
        
        # 1. فحص القيم المفقودة
        missing_percentage = (self.df.isnull().sum() / len(self.df)) * 100
        high_missing = missing_percentage[missing_percentage > 20].index.tolist()
        
        if high_missing:
            if lang == 'ar':
                warnings.append(f"⚠️ أعمدة بها قيم مفقودة >20%: {', '.join(high_missing[:3])}")
            else:
                warnings.append(f"⚠️ Columns with missing values >20%: {', '.join(high_missing[:3])}")
        
        # 2. فحص التكرارات
        duplicates = self.df.duplicated().sum()
        if duplicates > 0:
            if lang == 'ar':
                warnings.append(f"⚠️ يوجد {duplicates} سجل مكرر")
            else:
                warnings.append(f"⚠️ Found {duplicates} duplicate records")
        
        # 3. فحص القيم السلبية في المبالغ
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
    
    def _extract_insights(self):
        """استخلاص رؤى من بيانات المبيعات"""
        insights = []
        lang = st.session_state.get('language', 'ar')
        
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
                            insights.append(f"🏆 **أفضل منطقة مبيعات**: {top_region} (${top_sales:,.0f})")
                        else:
                            insights.append(f"🏆 **Top Sales Region**: {top_region} (${top_sales:,.0f})")
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
                            insights.append(f"📦 **أكثر منتج مبيعاً**: {top_product} ({top_qty:,} وحدة)")
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
        
        # تحليل هامش الربح
        if 'gross_margin' in self._calculate_kpis():
            margin = self._calculate_kpis()['gross_margin']['value']
            if lang == 'ar':
                if margin > 20:
                    insights.append(f"✅ **هامش ربح ممتاز**: {margin:.1f}% (أعلى من المتوسط)")
                elif margin > 10:
                    insights.append(f"⚠️ **هامش ربح متوسط**: {margin:.1f}% (بحاجة للتحسين)")
                else:
                    insights.append(f"❌ **هامش ربح منخفض**: {margin:.1f}% (تحتاج مراجعة)")
            else:
                if margin > 20:
                    insights.append(f"✅ **Excellent Profit Margin**: {margin:.1f}% (Above average)")
                elif margin > 10:
                    insights.append(f"⚠️ **Average Profit Margin**: {margin:.1f}% (Needs improvement)")
                else:
                    insights.append(f"❌ **Low Profit Margin**: {margin:.1f}% (Review needed)")
        
        return insights[:5]  # تقليل النقاط إلى 5 فقط
    
    def generate_professional_report(self, analysis_results):
        """إنشاء تقرير احترافي مختصر"""
        lang = st.session_state.get('language', 'ar')
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        if lang == 'ar':
            report = f"""
{'='*80}
تقرير تحليل المبيعات
{'='*80}

📅 تاريخ التقرير: {current_date}
📊 فترة التحليل: {self._get_date_range()}
👥 الجمهور المستهدف: {TranslationSystem.t('audience_target')}

{'-'*80}
الملخص التنفيذي
{'-'*80}

تم إجراء تحليل شامل لبيانات المبيعات لاستخلاص رؤى قابلة للتنفيذ.

• إجمالي المبيعات: {analysis_results['kpis'].get('total_sales', {}).get('formatted', 'غير متوفر')}
• عدد المعاملات: {analysis_results['kpis'].get('total_transactions', {}).get('formatted', 'غير متوفر')}
• هامش الربح الإجمالي: {analysis_results['kpis'].get('gross_margin', {}).get('formatted', 'غير متوفر')}

{'-'*80}
النقاط الرئيسية
{'-'*80}

"""
            for insight in analysis_results['insights']:
                report += f"• {insight.replace('**', '')}\n"
            
            report += f"""
{'-'*80}
تحليل هامش الربح
{'-'*80}

"""
            if 'gross_margin' in analysis_results['kpis']:
                margin = analysis_results['kpis']['gross_margin']['value']
                if margin > 20:
                    report += f"✅ هامش الربح ممتاز ({margin:.1f}%)\n"
                    report += "   (أعلى من متوسط الصناعة - حافظ على هذا الأداء)\n"
                elif margin > 10:
                    report += f"⚠️ هامش الربح متوسط ({margin:.1f}%)\n"
                    report += "   (بحاجة للتحسين - راجع تكاليف البضاعة)\n"
                else:
                    report += f"❌ هامش الربح منخفض ({margin:.1f}%)\n"
                    report += "   (يتطلب مراجعة عاجلة - راجع التسعير والتكاليف)\n"
            
            report += f"""
{'-'*80}
التوصيات الاستراتيجية
{'-'*80}

1. **تحسين هامش الربح**
   • راجع تكاليف البضاعة
   • عدل استراتيجية التسعير
   • قلل الخصومات غير الضرورية

2. **تعزيز المناطق عالية الأداء**
   • ركز التسويق على المناطق الرابحة
   • زود المخزون فيها

3. **استثمار أفضل المنتجات**
   • زد إنتاجية المنتجات الأكثر مبيعاً
   • طور منتجات مشابهة لها

{'-'*80}
جودة البيانات
{'-'*80}

"""
            if analysis_results['warnings']:
                report += "⚠️ تم اكتشاف بعض المشاكل:\n"
                for warning in analysis_results['warnings']:
                    report += f"• {warning}\n"
            else:
                report += "✅ جودة البيانات ممتازة - لا توجد مشاكل رئيسية\n"
            
            report += f"""
{'='*80}
نهاية التقرير
{'='*80}
"""
        else:
            report = f"""
{'='*80}
SALES ANALYSIS REPORT
{'='*80}

📅 Report Date: {current_date}
📊 Analysis Period: {self._get_date_range()}
👥 Target Audience: {TranslationSystem.t('audience_target')}

{'-'*80}
EXECUTIVE SUMMARY
{'-'*80}

Comprehensive sales data analysis conducted to extract actionable insights.

• Total Sales: {analysis_results['kpis'].get('total_sales', {}).get('formatted', 'N/A')}
• Total Transactions: {analysis_results['kpis'].get('total_transactions', {}).get('formatted', 'N/A')}
• Gross Margin: {analysis_results['kpis'].get('gross_margin', {}).get('formatted', 'N/A')}

{'-'*80}
KEY FINDINGS
{'-'*80}

"""
            for insight in analysis_results['insights']:
                report += f"• {insight.replace('**', '')}\n"
            
            report += f"""
{'-'*80}
GROSS MARGIN ANALYSIS
{'-'*80}

"""
            if 'gross_margin' in analysis_results['kpis']:
                margin = analysis_results['kpis']['gross_margin']['value']
                if margin > 20:
                    report += f"✅ Excellent Profit Margin ({margin:.1f}%)\n"
                    report += "   (Above industry average - Maintain this performance)\n"
                elif margin > 10:
                    report += f"⚠️ Average Profit Margin ({margin:.1f}%)\n"
                    report += "   (Needs improvement - Review cost of goods)\n"
                else:
                    report += f"❌ Low Profit Margin ({margin:.1f}%)\n"
                    report += "   (Requires urgent review - Check pricing and costs)\n"
            
            report += f"""
{'-'*80}
STRATEGIC RECOMMENDATIONS
{'-'*80}

1. **Improve Profit Margin**
   • Review cost of goods
   • Adjust pricing strategy
   • Reduce unnecessary discounts

2. **Enhance High-Performing Regions**
   • Focus marketing on profitable regions
   • Increase stock availability

3. **Invest in Top Products**
   • Increase production of best-selling products
   • Develop similar products

{'-'*80}
DATA QUALITY
{'-'*80}

"""
            if analysis_results['warnings']:
                report += "⚠️ Some issues detected:\n"
                for warning in analysis_results['warnings']:
                    report += f"• {warning}\n"
            else:
                report += "✅ Excellent data quality - No major issues found\n"
            
            report += f"""
{'='*80}
END OF REPORT
{'='*80}
"""
        
        return report
    
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
                        if st.session_state.get('language', 'ar') == 'ar':
                            return f"{min_date.strftime('%Y-%m-%d')} إلى {max_date.strftime('%Y-%m-%d')}"
                        else:
                            return f"{min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}"
                except:
                    pass
        
        if st.session_state.get('language', 'ar') == 'ar':
            return "غير متوفر"
        else:
            return "Not available"

# ==================== 3. وحدات مساعدة ====================

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
    """تحميل CSS مع دعم متعدد اللغات والوضع الغامق"""
    direction = TranslationSystem.get_language_direction()
    font_family = TranslationSystem.get_font_family()
    
    css = f"""
    <style>
    /* إعدادات عامة */
    .stApp {{
        font-family: {font_family};
        text-align: {direction};
        background-color: #0E1117;
        color: #FAFAFA;
    }}
    
    /* العنوان الرئيسي */
    .main-header {{
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        text-align: center;
        font-family: {font_family};
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }}
    
    /* بطاقات KPIs */
    .kpi-card {{
        background: #1F2937;
        border-radius: 12px;
        padding: 20px;
        margin: 10px;
        border: 1px solid #374151;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        text-align: center;
        transition: all 0.3s ease;
        font-family: {font_family};
        direction: {direction};
    }}
    
    .kpi-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        border-color: #3B82F6;
    }}
    
    /* صندوق الرفع */
    .upload-box {{
        border: 2px dashed #3B82F6;
        border-radius: 12px;
        padding: 40px;
        text-align: center;
        background: #111827;
        margin: 20px 0;
        font-family: {font_family};
        direction: {direction};
    }}
    
    /* بطاقات الملفات */
    .file-card {{
        background: #1F2937;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid #374151;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        font-family: {font_family};
        direction: {direction};
    }}
    
    /* صندوق التحذيرات */
    .warning-box {{
        background: #FEF3C7;
        border: 1px solid #F59E0B;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        font-family: {font_family};
        direction: {direction};
        color: #92400E;
    }}
    
    /* صندوق التقرير */
    .report-box {{
        background: #1F2937;
        border: 2px solid #3B82F6;
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
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        color: #D1D5DB;
    }}
    
    /* الأزرار */
    .stButton > button {{
        border-radius: 8px;
        font-family: {font_family};
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }}
    
    /* تحديدات */
    .stSelectbox, .stTextInput, .stNumberInput {{
        font-family: {font_family};
        background-color: #1F2937;
        color: #FAFAFA;
        border-color: #374151;
    }}
    
    /* تعريفات */
    .definition-text {{
        font-size: 0.85rem;
        color: #9CA3AF;
        margin-top: 5px;
        font-style: italic;
    }}
    
    /* تخصيص Streamlit */
    .css-1d391kg {{
        background-color: #0E1117;
    }}
    
    /* تحسينات للوضع الغامق */
    .css-1v3fvcr {{
        color: #FAFAFA;
    }}
    
    /* ألوان النصوص */
    h1, h2, h3, h4, h5, h6 {{
        color: #F3F4F6 !important;
    }}
    
    /* تخصيص علامات التبويب */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 24px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px 8px 0px 0px;
        padding: 10px 24px;
        font-weight: 600;
    }}
    </style>
    
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
    """
    st.markdown(css, unsafe_allow_html=True)

# ==================== 4. تهيئة حالة الجلسة ====================

# إعدادات الصفحة مع الوضع الغامق كافتراضي
st.set_page_config(
    page_title=TranslationSystem.t('dashboard_title'),
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تهيئة حالة الجلسة مع الوضع الغامق كافتراضي
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'
if 'language' not in st.session_state:
    st.session_state.language = 'ar'
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
if 'analysis_ready' not in st.session_state:
    st.session_state.analysis_ready = False

# تحميل CSS
load_css()

# ==================== 5. الشريط الجانبي ====================

with st.sidebar:
    st.markdown(f"### {TranslationSystem.t('sidebar_settings')}")
    
    # تبديل اللغة
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**{TranslationSystem.t('language')}**")
    with col2:
        current_lang = "English" if st.session_state.language == 'ar' else "العربية"
        if st.button(f"🌐 {current_lang}", use_container_width=True, key="language_toggle"):
            st.session_state.language = 'en' if st.session_state.language == 'ar' else 'ar'
            st.rerun()
    
    # تبديل المظهر
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**{TranslationSystem.t('theme')}**")
    with col2:
        current_theme = TranslationSystem.t('light_theme') if st.session_state.theme == 'dark' else TranslationSystem.t('dark_theme')
        if st.button(current_theme, use_container_width=True, key="theme_toggle"):
            st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
            st.rerun()
    
    st.divider()
    
    # تحميل الإعدادات السابقة
    if st.button(TranslationSystem.t('load_settings'), use_container_width=True, icon="📥", key="load_settings"):
        if os.path.exists('sales_config.json'):
            with open('sales_config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
                st.session_state.column_mapping = config.get('column_mapping', {})
                st.session_state.language = config.get('language', 'ar')
                st.session_state.theme = config.get('theme', 'dark')
                st.success(TranslationSystem.t('settings_loaded'))
                st.rerun()
        else:
            st.warning(TranslationSystem.t('no_settings'))
    
    # حفظ الإعدادات
    if st.session_state.column_mapping:
        if st.button(TranslationSystem.t('save_settings'), use_container_width=True, icon="💾", key="save_settings"):
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
    if st.button(TranslationSystem.t('reset'), use_container_width=True, icon="🔄", key="reset"):
        for key in list(st.session_state.keys()):
            if key not in ['language', 'theme']:
                del st.session_state[key]
        st.rerun()

# ==================== 6. العنوان الرئيسي ====================

st.markdown(f"""
<div class="main-header">
    <h1>{TranslationSystem.t('dashboard_title')}</h1>
    <p>{TranslationSystem.t('dashboard_subtitle')}</p>
    <p style="font-size: 0.9rem; opacity: 0.9;">{TranslationSystem.t('audience_target')}</p>
</div>
""", unsafe_allow_html=True)

# ==================== 7. تحميل الملفات ====================

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
            
            # دمج الملفات
            if len(dataframes) > 1:
                st.markdown("### 🔗 خيارات الدمج")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(TranslationSystem.t('merge_files'), use_container_width=True, icon="🔗", key="merge_button"):
                        merged_df = merge_dataframes(dataframes)
                        if merged_df is not None:
                            st.session_state.merged_df = merged_df
                            st.session_state.use_merged = True
                            st.session_state.current_df = merged_df
                            st.success(TranslationSystem.t('merged_success'))
                
                with col2:
                    if st.button(TranslationSystem.t('use_single'), use_container_width=True, icon="📄", key="single_button"):
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
            
            # عرض إحصائيات
            df_to_use = st.session_state.current_df
            
            if st.session_state.use_merged and st.session_state.merged_df is not None:
                st.info(f"📊 **{TranslationSystem.t('merged_data')}**: {len(df_to_use)} {TranslationSystem.t('rows')}, {len(df_to_use.columns)} {TranslationSystem.t('columns')}")
            else:
                st.info(f"📊 **{TranslationSystem.t('individual_file')}**: {len(df_to_use)} {TranslationSystem.t('rows')}, {len(df_to_use.columns)} {TranslationSystem.t('columns')}")
            
            # عرض عينة من البيانات
            with st.expander(f"{TranslationSystem.t('preview')} ({TranslationSystem.t('preview_rows')})"):
                st.dataframe(df_to_use.head(), use_container_width=True)
        
    except Exception as e:
        st.error(f"{TranslationSystem.t('upload_error')} {str(e)}")

# ==================== 8. تعيين الأعمدة ====================

if st.session_state.files_uploaded and st.session_state.current_df is not None:
    st.markdown(f"## 🎯 {TranslationSystem.t('step_2')}")
    
    df = st.session_state.current_df
    columns = df.columns.tolist()
    
    # استخدام AutoColumnMapper من الملف الآخر
    try:
        from sales_auto_column_mapper import SalesAutoColumnMapper
        mapper = SalesAutoColumnMapper(df)
        auto_suggestions = mapper.auto_detect_columns()
    except:
        # إذا فشل الاستيراد، ننشئ فئة مبسطة
        class SimpleMapper:
            def __init__(self, df):
                self.df = df
            
            def auto_detect_columns(self):
                return {}
        
        mapper = SimpleMapper(df)
        auto_suggestions = {}
    
    st.markdown(f"**{TranslationSystem.t('auto_detection')}**")
    st.info(TranslationSystem.t('auto_detection_desc'))
    
    # إنشاء تخطيط تعيين الأعمدة
    column_mapping = {}
    
    # عرض تعيين الأعمدة لكل فئة
    categories = {
        TranslationSystem.t('category_order'): ["order_id", "order_date", "status"],
        TranslationSystem.t('category_customer'): ["customer_name", "customer_id"],
        TranslationSystem.t('category_product'): ["product_name", "product_id", "category"],
        TranslationSystem.t('category_financial'): ["quantity", "total_amount", "discount", "cost"],
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
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(TranslationSystem.t('analyze_button'), type="primary", use_container_width=True, icon="🚀", key="analyze_button"):
            st.session_state.analysis_ready = True
            st.rerun()

# ==================== 9. التحليل الذكي ====================

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
    
    # بطاقات KPIs مع تعريفات
    kpis = analysis.get('kpis', {})
    if kpis:
        kpi_keys = list(kpis.keys())
        
        # عرض KPIs في أعمدة
        cols_per_row = 3
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
                            <div style="font-size: 1.8rem; font-weight: bold; color: #60A5FA;">
                                {kpi_info['formatted']}
                            </div>
                            <div style="color: #D1D5DB; font-size: 1rem; font-weight: 600;">
                                {kpi_info['label']}
                            </div>
                            <div class="definition-text">
                                {kpi_info.get('definition', '')}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
    
    # جودة البيانات
    if analysis.get('warnings'):
        st.markdown(f"### 🔍 {TranslationSystem.t('data_quality_title')}")
        for warning in analysis['warnings']:
            st.warning(warning)
    
    # النقاط الرئيسية
    if analysis.get('insights'):
        st.markdown(f"### 🎯 {TranslationSystem.t('key_findings')}")
        for insight in analysis['insights']:
            st.info(insight)
    
    # التقرير النصي الاحترافي
    st.markdown(f"### 📄 {TranslationSystem.t('report_title')}")
    
    # زر إنشاء التقرير
    if st.button(TranslationSystem.t('generate_report'), use_container_width=True, icon="📋", type="primary", key="generate_report"):
        st.session_state.text_report = analyzer.generate_professional_report(analysis)
    
    # عرض التقرير إذا كان موجوداً
    if st.session_state.text_report:
        st.markdown(f"#### {TranslationSystem.t('executive_summary')}")
        
        # صندوق عرض التقرير
        st.markdown(f'<div class="report-box">{st.session_state.text_report}</div>', unsafe_allow_html=True)
        
        # زر النسخ
        if st.button(TranslationSystem.t('copy_report'), use_container_width=True, icon="📋", key="copy_report"):
            try:
                import pyperclip
                pyperclip.copy(st.session_state.text_report)
                st.success(TranslationSystem.t('report_copied'))
            except:
                st.code(st.session_state.text_report, language='text')
                if st.session_state.language == 'ar':
                    st.warning("⚠️ يرجى نسخ النص أعلاه يدوياً")
                else:
                    st.warning("⚠️ Please copy the text above manually")

# ==================== 10. رسالة الترحيب ====================

if not st.session_state.files_uploaded:
    st.info("""
    📋 **إرشادات الاستخدام:**
    
    1. **رفع الملفات**: قم برفع ملفات Excel أو CSV تحتوي على بيانات المبيعات
    2. **تعيين الأعمدة**: سيقوم النظام بالتعرف التلقائي على أعمدة البيانات
    3. **التحليل**: انتقل إلى التحليل للحصول على نتائج ورسوم بيانية
    4. **التقرير**: إنشاء تقرير نصي احترافي يمكن نسخه للعميل
    
    💡 **مميزات المنتج**:
    - تحليل احترافي مصمم للشركات الصغيرة والمتوسطة
    - واجهة غامقة مع نصوص واضحة
    - تقارير مكتوبة باللغة العربية أو الإنجليزية بالكامل
    - نتائج قابلة للتنفيذ فوراً
    """)

# ==================== 11. تذييل الصفحة ====================

st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="text-align: center; color: #6B7280; font-size: 0.9rem;">
    <p>📊 نظام تحليل المبيعات الذكي | الإصدار 3.0 | يدعم العربية والإنجليزية</p>
    <p>تم تطوير المنتج للشركات الصغيرة والمتوسطة لتحليل بيانات المبيعات بسرعة ووضوح</p>
    </div>
    """, unsafe_allow_html=True)