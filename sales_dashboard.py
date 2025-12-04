"""
لوحة تحكم المبيعات الذكية - ملف واحد موحد
يحتوي على جميع الوحدات: التعرف التلقائي، التحليل، الرسوم البيانية، ولوحة التحكم
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import re
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from io import BytesIO

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
            
            # البحث عن تطابقات في الأنماط
            for field_type, patterns_info in self.column_patterns.items():
                # البحث في الأنماط
                for pattern in patterns_info['patterns']:
                    if re.search(pattern, column_lower, re.IGNORECASE):
                        suggestions[field_type] = column
                        break
                
                # البحث في الكلمات المفتاحية
                if field_type not in suggestions:
                    for keyword in patterns_info['keywords']:
                        if keyword.lower() in column_lower:
                            suggestions[field_type] = column
                            break
            
            # محاولة التعرف على التواريخ
            if self._is_date_column(column):
                if 'order_date' not in suggestions:
                    suggestions['order_date'] = column
                elif 'delivery_date' not in suggestions:
                    suggestions['delivery_date'] = column
        
        return suggestions
    
    def _is_date_column(self, column_name):
        """فحص إذا كان العمود يحتوي على تواريخ"""
        if column_name not in self.df.columns:
            return False
        
        column_sample = self.df[column_name].dropna().head(10)
        
        if len(column_sample) == 0:
            return False
        
        # محاولة التحويل إلى تاريخ
        try:
            # إذا كان النوع بالفعل datetime
            if pd.api.types.is_datetime64_any_dtype(self.df[column_name]):
                return True
            
            # اختبار التحويل
            test_dates = pd.to_datetime(column_sample, errors='coerce')
            success_rate = test_dates.notna().sum() / len(column_sample)
            
            return success_rate > 0.7  # إذا نجح في 70% من الحالات
        except:
            return False
    
    def suggest_column_types(self):
        """اقتراح أنواع البيانات للأعمدة"""
        column_types = {}
        
        for column in self.df.columns:
            dtype = str(self.df[column].dtype)
            
            # فحص النوع
            if pd.api.types.is_numeric_dtype(self.df[column]):
                column_types[column] = 'numeric'
            elif pd.api.types.is_datetime64_any_dtype(self.df[column]):
                column_types[column] = 'date'
            elif self._is_categorical_column(column):
                column_types[column] = 'categorical'
            else:
                column_types[column] = 'text'
        
        return column_types
    
    def _is_categorical_column(self, column_name, max_unique_ratio=0.3):
        """فحص إذا كان العمود فئوي"""
        unique_count = self.df[column_name].nunique()
        total_count = len(self.df[column_name].dropna())
        
        if total_count == 0:
            return False
        
        unique_ratio = unique_count / total_count
        return unique_ratio <= max_unique_ratio and unique_count < 50

# ==================== 2. وحدة التحليل الذكي ====================

class SalesDataAnalyzer:
    def __init__(self, dataframe, column_mapping):
        self.df = dataframe.copy()
        self.mapping = column_mapping
        self.reverse_mapping = {v: k for k, v in column_mapping.items() if v != "❌ لا يوجد"}
    
    def analyze_all(self):
        """إجراء جميع التحليلات المتاحة للمبيعات"""
        analysis_results = {
            'kpis': {},
            'distributions': {},
            'trends': {},
            'insights': [],
            'warnings': []
        }
        
        # 1. تحليل KPIs
        analysis_results['kpis'] = self._calculate_kpis()
        
        # 2. توزيع البيانات
        analysis_results['distributions'] = self._analyze_distributions()
        
        # 3. تحليل الاتجاهات
        analysis_results['trends'] = self._analyze_trends()
        
        # 4. استخلاص Insights
        analysis_results['insights'] = self._extract_insights()
        
        # 5. التحذيرات
        analysis_results['warnings'] = self._check_data_quality()
        
        return analysis_results
    
    def _calculate_kpis(self):
        """حساب مؤشرات أداء المبيعات"""
        kpis = {}
        
        # إجمالي عدد المعاملات
        total_transactions = len(self.df)
        kpis['total_transactions'] = {
            'value': f"{total_transactions:,}",
            'label': 'إجمالي المعاملات',
            'icon': '🛒'
        }
        
        # إجمالي المبيعات
        if 'total_amount' in self.mapping:
            amount_col = self.mapping['total_amount']
            if amount_col in self.df.columns:
                try:
                    self.df[amount_col] = pd.to_numeric(self.df[amount_col], errors='coerce')
                    total_sales = self.df[amount_col].sum()
                    kpis['total_sales'] = {
                        'value': f"${total_sales:,.0f}",
                        'label': 'إجمالي المبيعات',
                        'icon': '💰'
                    }
                    
                    # متوسط قيمة المعاملة
                    avg_transaction = total_sales / total_transactions
                    kpis['avg_transaction'] = {
                        'value': f"${avg_transaction:,.0f}",
                        'label': 'متوسط قيمة المعاملة',
                        'icon': '📊'
                    }
                except:
                    pass
        
        # إجمالي الربح
        if 'profit' in self.mapping:
            profit_col = self.mapping['profit']
            if profit_col in self.df.columns:
                try:
                    self.df[profit_col] = pd.to_numeric(self.df[profit_col], errors='coerce')
                    total_profit = self.df[profit_col].sum()
                    kpis['total_profit'] = {
                        'value': f"${total_profit:,.0f}",
                        'label': 'إجمالي الربح',
                        'icon': '📈'
                    }
                except:
                    pass
        
        # عدد العملاء الفريدين
        if 'customer_id' in self.mapping:
            customer_col = self.mapping['customer_id']
            if customer_col in self.df.columns:
                unique_customers = self.df[customer_col].nunique()
                kpis['unique_customers'] = {
                    'value': f"{unique_customers:,}",
                    'label': 'عدد العملاء',
                    'icon': '👥'
                }
        
        # عدد المنتجات الفريدة
        if 'product_id' in self.mapping:
            product_col = self.mapping['product_id']
            if product_col in self.df.columns:
                unique_products = self.df[product_col].nunique()
                kpis['unique_products'] = {
                    'value': f"{unique_products:,}",
                    'label': 'عدد المنتجات',
                    'icon': '📦'
                }
        
        # متوسط الكمية لكل معاملة
        if 'quantity' in self.mapping:
            quantity_col = self.mapping['quantity']
            if quantity_col in self.df.columns:
                try:
                    self.df[quantity_col] = pd.to_numeric(self.df[quantity_col], errors='coerce')
                    avg_quantity = self.df[quantity_col].mean()
                    kpis['avg_quantity'] = {
                        'value': f"{avg_quantity:.1f}",
                        'label': 'متوسط الكمية',
                        'icon': '⚖️'
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
                    self.df[amount_col] = pd.to_numeric(self.df[amount_col], errors='coerce')
                    
                    total_discount = self.df[discount_col].sum()
                    total_sales_before_discount = self.df[amount_col].sum() + total_discount
                    
                    if total_sales_before_discount > 0:
                        discount_rate = (total_discount / total_sales_before_discount) * 100
                        kpis['discount_rate'] = {
                            'value': f"{discount_rate:.1f}%",
                            'label': 'معدل الخصم',
                            'icon': '🎯'
                        }
                except:
                    pass
        
        return kpis
    
    def _analyze_distributions(self):
        """تحليل توزيع بيانات المبيعات"""
        distributions = {}
        
        # توزيع المناطق
        if 'region' in self.mapping:
            region_col = self.mapping['region']
            if region_col in self.df.columns:
                region_dist = self.df[region_col].value_counts().to_dict()
                distributions['region'] = region_dist
        
        # توزيع الفئات
        if 'category' in self.mapping:
            category_col = self.mapping['category']
            if category_col in self.df.columns:
                category_dist = self.df[category_col].value_counts().to_dict()
                distributions['category'] = category_dist
        
        # توزيع المنتجات (أعلى 10)
        if 'product_name' in self.mapping:
            product_col = self.mapping['product_name']
            if product_col in self.df.columns:
                product_dist = self.df[product_col].value_counts().head(10).to_dict()
                distributions['top_products'] = product_dist
        
        # توزيع طرق الدفع
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
                    # تحويل التواريخ
                    df_copy = self.df.copy()
                    df_copy[date_col] = pd.to_datetime(df_copy[date_col], errors='coerce')
                    df_copy[amount_col] = pd.to_numeric(df_copy[amount_col], errors='coerce')
                    
                    # تنظيف البيانات
                    df_clean = df_copy.dropna(subset=[date_col, amount_col])
                    
                    if len(df_clean) > 0:
                        # الاتجاه الشهري
                        df_clean['year_month'] = df_clean[date_col].dt.to_period('M')
                        monthly_trend = df_clean.groupby('year_month')[amount_col].agg(['sum', 'count']).reset_index()
                        monthly_trend['year_month'] = monthly_trend['year_month'].astype(str)
                        
                        trends['monthly'] = monthly_trend.to_dict('records')
                        
                        # النمو الشهري
                        if len(monthly_trend) > 1:
                            monthly_trend['growth'] = monthly_trend['sum'].pct_change() * 100
                            trends['growth'] = monthly_trend[['year_month', 'growth']].dropna().to_dict('records')
                except:
                    pass
        
        return trends
    
    def _extract_insights(self):
        """استخلاص رؤى من بيانات المبيعات"""
        insights = []
        
        # 1. أفضل منطقة مبيعات
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
                        insights.append(f"🏆 **أفضل منطقة مبيعات**: {top_region} (${top_sales:,.0f})")
                except:
                    pass
        
        # 2. أفضل منتج
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
                        insights.append(f"📦 **أكثر منتج مبيعاً**: {top_product} ({top_qty:,} وحدة)")
                except:
                    pass
        
        # 3. أفضل مندوب مبيعات
        if 'salesperson' in self.mapping and 'total_amount' in self.mapping:
            salesperson_col = self.mapping['salesperson']
            amount_col = self.mapping['total_amount']
            
            if salesperson_col in self.df.columns and amount_col in self.df.columns:
                try:
                    self.df[amount_col] = pd.to_numeric(self.df[amount_col], errors='coerce')
                    salesperson_performance = self.df.groupby(salesperson_col)[amount_col].sum().sort_values(ascending=False)
                    
                    if len(salesperson_performance) > 0:
                        top_salesperson = salesperson_performance.index[0]
                        top_amount = salesperson_performance.iloc[0]
                        insights.append(f"👨‍💼 **أفضل مندوب مبيعات**: {top_salesperson} (${top_amount:,.0f})")
                except:
                    pass
        
        # 4. تحليل الربحية
        if 'profit' in self.mapping:
            profit_col = self.mapping['profit']
            if profit_col in self.df.columns:
                try:
                    self.df[profit_col] = pd.to_numeric(self.df[profit_col], errors='coerce')
                    profitable_transactions = (self.df[profit_col] > 0).sum()
                    total_transactions = len(self.df)
                    profitability_rate = (profitable_transactions / total_transactions) * 100
                    
                    insights.append(f"📊 **معدل الربحية**: {profitability_rate:.1f}% من المعاملات مربحة")
                except:
                    pass
        
        # 5. تحليل التكرار
        if 'customer_id' in self.mapping:
            customer_col = self.mapping['customer_id']
            if customer_col in self.df.columns:
                repeat_customers = self.df[customer_col].duplicated().sum()
                if repeat_customers > 0:
                    repeat_rate = (repeat_customers / len(self.df)) * 100
                    insights.append(f"🔄 **معدل التكرار**: {repeat_rate:.1f}% من العملاء متكررون")
        
        return insights
    
    def _check_data_quality(self):
        """فحص جودة بيانات المبيعات"""
        warnings = []
        
        # 1. فحص القيم المفقودة
        missing_percentage = (self.df.isnull().sum() / len(self.df)) * 100
        high_missing = missing_percentage[missing_percentage > 20].index.tolist()
        
        if high_missing:
            warnings.append(f"⚠️ أعمدة بها قيم مفقودة >20%: {', '.join(high_missing)}")
        
        # 2. فحص التكرارات
        duplicates = self.df.duplicated().sum()
        if duplicates > 0:
            warnings.append(f"⚠️ يوجد {duplicates} سجل مكرر")
        
        # 3. فحص القيم السلبية في المبالغ
        if 'total_amount' in self.mapping:
            amount_col = self.mapping['total_amount']
            if amount_col in self.df.columns:
                try:
                    amount_data = pd.to_numeric(self.df[amount_col], errors='coerce')
                    negative_amounts = (amount_data < 0).sum()
                    if negative_amounts > 0:
                        warnings.append(f"⚠️ يوجد {negative_amounts} معاملة بمبلغ سالب")
                except:
                    pass
        
        # 4. فحص الكميات غير المنطقية
        if 'quantity' in self.mapping:
            quantity_col = self.mapping['quantity']
            if quantity_col in self.df.columns:
                try:
                    quantity_data = pd.to_numeric(self.df[quantity_col], errors='coerce')
                    # كميات سالبة أو صفر
                    invalid_quantities = ((quantity_data <= 0) | (quantity_data > 1000)).sum()
                    if invalid_quantities > 0:
                        warnings.append(f"⚠️ يوجد {invalid_quantities} معاملة بكمية غير منطقية")
                except:
                    pass
        
        # 5. فحص التواريخ غير المنطقية
        if 'order_date' in self.mapping:
            date_col = self.mapping['order_date']
            if date_col in self.df.columns:
                try:
                    dates = pd.to_datetime(self.df[date_col], errors='coerce')
                    future_dates = dates[dates > pd.Timestamp.now()]
                    if len(future_dates) > 0:
                        warnings.append(f"⚠️ يوجد {len(future_dates)} معاملة بتاريخ مستقبلي")
                except:
                    pass
        
        return warnings
    
    def get_modified_dataframe(self):
        """الحصول على البيانات بعد التعديل"""
        return self.df
    
    def generate_report(self):
        """توليد تقرير نصي عن تحليل المبيعات"""
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("تقرير تحليل بيانات المبيعات")
        report_lines.append(f"تاريخ التوليد: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report_lines.append("=" * 60)
        report_lines.append("")
        
        # معلومات عامة
        report_lines.append("معلومات عامة:")
        report_lines.append(f"- عدد المعاملات: {len(self.df)}")
        report_lines.append(f"- عدد الأعمدة: {len(self.df.columns)}")
        report_lines.append("")
        
        # KPIs
        kpis = self._calculate_kpis()
        report_lines.append("المؤشرات الرئيسية (KPIs):")
        for kpi_name, kpi_info in kpis.items():
            report_lines.append(f"- {kpi_info['label']}: {kpi_info['value']}")
        report_lines.append("")
        
        # Insights
        insights = self._extract_insights()
        if insights:
            report_lines.append("الرؤى المستخلصة:")
            for insight in insights:
                report_lines.append(f"- {insight}")
            report_lines.append("")
        
        # Warnings
        warnings = self._check_data_quality()
        if warnings:
            report_lines.append("تحذيرات جودة البيانات:")
            for warning in warnings:
                report_lines.append(f"- {warning}")
            report_lines.append("")
        
        # Recommendations
        report_lines.append("التوصيات:")
        report_lines.append("1. التركيز على المناطق ذات الأداء العالي")
        report_lines.append("2. تحليل أسباب المبيعات المنخفضة في المناطق الضعيفة")
        report_lines.append("3. تحسين المنتجات الأكثر مبيعاً")
        report_lines.append("4. تحفيز مندوبي المبيعات بناءً على الأداء")
        report_lines.append("5. تحليل تأثير الخصومات على المبيعات")
        
        return "\n".join(report_lines)

# ==================== 3. وحدة الرسوم البيانية ====================

class SalesVisualizer:
    def __init__(self, dataframe, column_mapping, analysis_results):
        self.df = dataframe
        self.mapping = column_mapping
        self.analysis = analysis_results
    
    def generate_all_charts(self):
        """توليد جميع الرسوم البيانية الممكنة للمبيعات"""
        charts = []
        
        # 1. إجمالي المبيعات عبر الزمن
        if 'order_date' in self.mapping and 'total_amount' in self.mapping:
            sales_trend_chart = self._create_sales_trend_chart()
            if sales_trend_chart:
                charts.append(sales_trend_chart)
        
        # 2. أفضل المنتجات مبيعاً
        if 'product_name' in self.mapping and 'quantity' in self.mapping:
            top_products_chart = self._create_top_products_chart()
            if top_products_chart:
                charts.append(top_products_chart)
        
        # 3. توزيع المبيعات حسب المنطقة
        if 'region' in self.mapping and 'total_amount' in self.mapping:
            region_chart = self._create_region_chart()
            if region_chart:
                charts.append(region_chart)
        
        # 4. توزيع المبيعات حسب الفئة
        if 'category' in self.mapping and 'total_amount' in self.mapping:
            category_chart = self._create_category_chart()
            if category_chart:
                charts.append(category_chart)
        
        # 5. أداء مندوبي المبيعات
        if 'salesperson' in self.mapping and 'total_amount' in self.mapping:
            salesperson_chart = self._create_salesperson_chart()
            if salesperson_chart:
                charts.append(salesperson_chart)
        
        # 6. علاقة السعر بالكمية
        if 'price' in self.mapping and 'quantity' in self.mapping:
            price_quantity_chart = self._create_price_quantity_chart()
            if price_quantity_chart:
                charts.append(price_quantity_chart)
        
        # 7. توزيع طرق الدفع
        if 'payment_method' in self.mapping:
            payment_chart = self._create_payment_method_chart()
            if payment_chart:
                charts.append(payment_chart)
        
        # 8. تحليل الربحية
        if 'profit' in self.mapping:
            profit_chart = self._create_profit_chart()
            if profit_chart:
                charts.append(profit_chart)
        
        return charts
    
    def _create_sales_trend_chart(self):
        """إنشاء رسم اتجاه المبيعات عبر الزمن"""
        date_col = self.mapping['order_date']
        amount_col = self.mapping['total_amount']
        
        if date_col not in self.df.columns or amount_col not in self.df.columns:
            return None
        
        try:
            # إنشاء نسخة من البيانات
            df_copy = self.df.copy()
            
            # تحويل التواريخ
            df_copy[date_col] = pd.to_datetime(df_copy[date_col], errors='coerce')
            df_copy[amount_col] = pd.to_numeric(df_copy[amount_col], errors='coerce')
            
            # إزالة القيم الفارغة
            df_clean = df_copy.dropna(subset=[date_col, amount_col])
            
            if len(df_clean) == 0:
                return None
            
            # تجميع البيانات حسب التاريخ (يومي/شهري)
            df_clean['date_trunc'] = df_clean[date_col].dt.to_period('M').dt.to_timestamp()
            sales_trend = df_clean.groupby('date_trunc')[amount_col].sum().reset_index()
            
            # إنشاء الخط البياني
            fig = px.line(
                sales_trend,
                x='date_trunc',
                y=amount_col,
                title='اتجاه المبيعات الشهرية',
                labels={'date_trunc': 'الشهر', amount_col: 'إجمالي المبيعات'}
            )
            
            # إضافة نقاط
            fig.update_traces(mode='lines+markers')
            
            return {
                'title': 'اتجاه المبيعات الشهرية',
                'figure': fig,
                'available': True
            }
            
        except:
            return None
    
    def _create_top_products_chart(self):
        """إنشاء رسم أفضل المنتجات مبيعاً"""
        product_col = self.mapping['product_name']
        quantity_col = self.mapping['quantity']
        
        if product_col not in self.df.columns or quantity_col not in self.df.columns:
            return None
        
        try:
            # تحويل الكميات إلى أرقام
            df_copy = self.df.copy()
            df_copy[quantity_col] = pd.to_numeric(df_copy[quantity_col], errors='coerce')
            
            # تجميع حسب المنتج
            product_sales = df_copy.groupby(product_col)[quantity_col].sum().reset_index()
            product_sales = product_sales.sort_values(quantity_col, ascending=False).head(10)
            
            # إنشاء الرسم البياني الشريطي
            fig = px.bar(
                product_sales,
                x=quantity_col,
                y=product_col,
                orientation='h',
                color=quantity_col,
                color_continuous_scale='Viridis',
                title='أفضل 10 منتجات مبيعاً'
            )
            
            fig.update_layout(
                xaxis_title='الكمية المباعة',
                yaxis_title='المنتج',
                coloraxis_showscale=False
            )
            
            return {
                'title': 'أفضل المنتجات مبيعاً',
                'figure': fig,
                'available': True
            }
            
        except:
            return None
    
    def _create_region_chart(self):
        """إنشاء رسم توزيع المبيعات حسب المنطقة"""
        region_col = self.mapping['region']
        amount_col = self.mapping['total_amount']
        
        if region_col not in self.df.columns or amount_col not in self.df.columns:
            return None
        
        try:
            # تحويل المبالغ إلى أرقام
            df_copy = self.df.copy()
            df_copy[amount_col] = pd.to_numeric(df_copy[amount_col], errors='coerce')
            
            # تجميع حسب المنطقة
            region_sales = df_copy.groupby(region_col)[amount_col].sum().reset_index()
            region_sales = region_sales.sort_values(amount_col, ascending=False)
            
            # إنشاء مخطط دائري
            fig = px.pie(
                region_sales,
                values=amount_col,
                names=region_col,
                title='توزيع المبيعات حسب المنطقة',
                hole=0.4
            )
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            
            return {
                'title': 'توزيع المبيعات حسب المنطقة',
                'figure': fig,
                'available': True
            }
            
        except:
            return None
    
    def _create_category_chart(self):
        """إنشاء رسم توزيع المبيعات حسب الفئة"""
        category_col = self.mapping['category']
        amount_col = self.mapping['total_amount']
        
        if category_col not in self.df.columns or amount_col not in self.df.columns:
            return None
        
        try:
            # تحويل المبالغ إلى أرقام
            df_copy = self.df.copy()
            df_copy[amount_col] = pd.to_numeric(df_copy[amount_col], errors='coerce')
            
            # تجميع حسب الفئة
            category_sales = df_copy.groupby(category_col)[amount_col].sum().reset_index()
            category_sales = category_sales.sort_values(amount_col, ascending=False).head(8)
            
            # إنشاء الرسم البياني
            fig = px.bar(
                category_sales,
                x=category_col,
                y=amount_col,
                color=amount_col,
                color_continuous_scale='Blues',
                title='توزيع المبيعات حسب الفئة'
            )
            
            fig.update_layout(
                xaxis_title='الفئة',
                yaxis_title='إجمالي المبيعات',
                coloraxis_showscale=False
            )
            
            return {
                'title': 'توزيع المبيعات حسب الفئة',
                'figure': fig,
                'available': True
            }
            
        except:
            return None
    
    def _create_salesperson_chart(self):
        """إنشاء رسم أداء مندوبي المبيعات"""
        salesperson_col = self.mapping['salesperson']
        amount_col = self.mapping['total_amount']
        
        if salesperson_col not in self.df.columns or amount_col not in self.df.columns:
            return None
        
        try:
            # تحويل المبالغ إلى أرقام
            df_copy = self.df.copy()
            df_copy[amount_col] = pd.to_numeric(df_copy[amount_col], errors='coerce')
            
            # تجميع حسب المندوب
            salesperson_performance = df_copy.groupby(salesperson_col)[amount_col].sum().reset_index()
            salesperson_performance = salesperson_performance.sort_values(amount_col, ascending=False).head(10)
            
            # إنشاء الرسم البياني
            fig = px.bar(
                salesperson_performance,
                x=salesperson_col,
                y=amount_col,
                color=amount_col,
                color_continuous_scale='RdYlGn',
                title='أفضل 10 مندوبي مبيعات'
            )
            
            fig.update_layout(
                xaxis_title='مندوب المبيعات',
                yaxis_title='إجمالي المبيعات',
                coloraxis_showscale=False
            )
            
            return {
                'title': 'أداء مندوبي المبيعات',
                'figure': fig,
                'available': True
            }
            
        except:
            return None
    
    def _create_price_quantity_chart(self):
        """إنشاء رسم علاقة السعر بالكمية"""
        price_col = self.mapping['price']
        quantity_col = self.mapping['quantity']
        
        if price_col not in self.df.columns or quantity_col not in self.df.columns:
            return None
        
        try:
            # تحويل البيانات إلى أرقام
            df_copy = self.df.copy()
            df_copy[price_col] = pd.to_numeric(df_copy[price_col], errors='coerce')
            df_copy[quantity_col] = pd.to_numeric(df_copy[quantity_col], errors='coerce')
            
            # تنظيف البيانات
            df_clean = df_copy.dropna(subset=[price_col, quantity_col])
            
            if len(df_clean) == 0:
                return None
            
            # إنشاء مخطط التبعثر
            fig = px.scatter(
                df_clean,
                x=price_col,
                y=quantity_col,
                trendline="ols",
                title='العلاقة بين السعر والكمية المباعة',
                labels={price_col: 'السعر', quantity_col: 'الكمية المباعة'}
            )
            
            # حساب معامل الارتباط
            correlation = df_clean[[price_col, quantity_col]].corr().iloc[0,1]
            
            # إضافة نص معامل الارتباط
            fig.add_annotation(
                x=0.05, y=0.95,
                xref="paper", yref="paper",
                text=f"معامل الارتباط: {correlation:.2f}",
                showarrow=False,
                bgcolor="white",
                bordercolor="black",
                borderwidth=1
            )
            
            return {
                'title': 'العلاقة بين السعر والكمية',
                'figure': fig,
                'available': True
            }
            
        except:
            return None
    
    def _create_payment_method_chart(self):
        """إنشاء رسم توزيع طرق الدفع"""
        payment_col = self.mapping['payment_method']
        
        if payment_col not in self.df.columns:
            return None
        
        # حساب التوزيع
        payment_counts = self.df[payment_col].value_counts().reset_index()
        payment_counts.columns = ['payment_method', 'count']
        
        # إنشاء مخطط دائري
        fig = px.pie(
            payment_counts,
            values='count',
            names='payment_method',
            title='توزيع طرق الدفع',
            hole=0.3
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        
        return {
            'title': 'توزيع طرق الدفع',
            'figure': fig,
            'available': True
        }
    
    def _create_profit_chart(self):
        """إنشاء رسم تحليل الربحية"""
        profit_col = self.mapping['profit']
        
        if profit_col not in self.df.columns:
            return None
        
        try:
            # تحويل الأرباح إلى أرقام
            profit_data = pd.to_numeric(self.df[profit_col], errors='coerce').dropna()
            
            if len(profit_data) == 0:
                return None
            
            # إنشاء histogram
            fig = px.histogram(
                profit_data,
                nbins=30,
                title='توزيع الأرباح',
                labels={'value': 'الربح', 'count': 'عدد المعاملات'}
            )
            
            # إضافة خط للمتوسط
            avg_profit = profit_data.mean()
            fig.add_vline(
                x=avg_profit,
                line_dash="dash",
                line_color="green",
                annotation_text=f"المتوسط: ${avg_profit:,.0f}",
                annotation_position="top right"
            )
            
            # إضافة خط للصفر
            fig.add_vline(
                x=0,
                line_dash="dot",
                line_color="red",
                annotation_text="نقطة التعادل",
                annotation_position="bottom right"
            )
            
            return {
                'title': 'توزيع الأرباح',
                'figure': fig,
                'available': True
            }
            
        except:
            return None

# ==================== 4. نظام الترجمة الكامل ====================

class SalesTranslationSystem:
    """نظام الترجمة ثنائي اللغة للمبيعات"""
    
    translations = {
        'ar': {
            # العنوان الرئيسي
            'main_title': '📈 لوحة تحكم المبيعات الذكية',
            'main_subtitle': 'تعمل مع <strong>عدة ملفات Excel</strong> - قم برفع ملفاتك وسنحلل بيانات المبيعات تلقائياً',
            
            # الشريط الجانبي
            'sidebar_settings': '⚙️ إعدادات',
            'sidebar_language': 'اللغة:',
            'sidebar_theme': 'المظهر:',
            'sidebar_load_settings': '📥 تحميل إعدادات سابقة',
            'sidebar_save_settings': '💾 حفظ الإعدادات',
            'sidebar_load_success': 'تم تحميل الإعدادات السابقة',
            'sidebar_save_success': 'تم حفظ الإعدادات',
            'sidebar_no_settings': 'لا توجد إعدادات سابقة',
            
            # رفع الملفات
            'upload_title': '📤 الخطوة 1: رفع ملفات المبيعات',
            'upload_placeholder': 'اسحب وأفلت ملفات Excel هنا أو انقر للاختيار',
            'upload_help': 'يدعم الملفات: Excel (.xlsx, .xls), CSV',
            'upload_success': '✅ تم تحميل {count} ملف بنجاح!',
            'upload_error': '❌ خطأ في تحميل الملف:',
            'preview_data': '👀 معاينة البيانات (أول 5 صفوف)',
            'merge_files': '🔗 دمج الملفات',
            'merged_success': '✅ تم دمج الملفات بنجاح!',
            'select_files': 'اختر ملفات',
            
            # إحصائيات
            'stats_records': 'عدد السجلات',
            'stats_columns': 'عدد الأعمدة',
            'stats_numeric': 'أعمدة رقمية',
            'stats_files': 'عدد الملفات',
            
            # تعيين الأعمدة
            'mapping_title': '🎯 الخطوة 2: تعيين الأعمدة',
            'mapping_auto': '💡 <strong>التعرف التلقائي</strong>: النظام حاول تخمين أنواع الأعمدة. يمكنك تعديلها يدوياً إذا كانت غير صحيحة.',
            
            # فئات الأعمدة
            'cat_order_info': 'معلومات الطلب',
            'cat_customer_info': 'معلومات العميل',
            'cat_product_info': 'معلومات المنتج',
            'cat_financial': 'المعلومات المالية',
            'cat_location': 'الموقع',
            'cat_sales_info': 'معلومات المبيعات',
            
            # أسماء الحقول
            'field_order_id': 'رقم الطلب',
            'field_customer_name': 'اسم العميل',
            'field_customer_id': 'رقم العميل',
            'field_product_name': 'اسم المنتج',
            'field_product_id': 'رقم المنتج',
            'field_category': 'الفئة',
            'field_quantity': 'الكمية',
            'field_unit_price': 'سعر الوحدة',
            'field_total_price': 'إجمالي السعر',
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
            
            # زر التحليل
            'analyze_button': '🚀 انتقل إلى التحليل',
            
            # نتائج التحليل
            'analysis_title': '📊 الخطوة 3: تحليل بيانات المبيعات',
            'kpis_title': '📈 النتائج الرئيسية',
            'charts_title': '📊 الرسوم البيانية التلقائية',
            'advanced_title': '🔍 تحليل متقدم',
            'correlations_title': 'العلاقات بين المتغيرات',
            'outliers_title': 'اكتشاف القيم الشاذة',
            'outliers_found': 'تم اكتشاف {} قيمة شاذة في المبيعات',
            'no_outliers': '✅ لم يتم اكتشاف قيم شاذة في المبيعات',
            'zero_std': 'انحراف المبيعات المعياري صفر، لا يمكن اكتشاف قيم شاذة',
            
            # تصدير
            'export_data': '📥 تحميل البيانات المعدلة (CSV)',
            'export_report': '📄 تحميل التقرير الكامل',
            'download_csv': '⬇️ انقر للتحميل',
            'download_report': '⬇️ انقر للتحميل',
            
            # رسائل أخرى
            'loading': 'جاري التحميل...',
            'not_available': 'غير متوفر',
            'file_info': '📄 معلومات الملف',
            'total_rows': 'إجمالي الصفوف',
            'total_columns': 'إجمالي الأعمدة',
            'merged_data': 'بيانات مدمجة',
            'individual_files': 'ملفات فردية',
        },
        'en': {
            # Main Title
            'main_title': '📈 Smart Sales Analytics Dashboard',
            'main_subtitle': 'Works with <strong>multiple Excel files</strong> - Upload your files and we will automatically analyze sales data',
            
            # Sidebar
            'sidebar_settings': '⚙️ Settings',
            'sidebar_language': 'Language:',
            'sidebar_theme': 'Theme:',
            'sidebar_load_settings': '📥 Load Previous Settings',
            'sidebar_save_settings': '💾 Save Settings',
            'sidebar_load_success': 'Previous settings loaded',
            'sidebar_save_success': 'Settings saved',
            'sidebar_no_settings': 'No previous settings',
            
            # File Upload
            'upload_title': '📤 Step 1: Upload Sales Files',
            'upload_placeholder': 'Drag and drop Excel files here or click to browse',
            'upload_help': 'Supports: Excel (.xlsx, .xls), CSV',
            'upload_success': '✅ {count} files uploaded successfully!',
            'upload_error': '❌ Error loading file:',
            'preview_data': '👀 Data Preview (First 5 rows)',
            'merge_files': '🔗 Merge Files',
            'merged_success': '✅ Files merged successfully!',
            'select_files': 'Select Files',
            
            # Statistics
            'stats_records': 'Number of Records',
            'stats_columns': 'Number of Columns',
            'stats_numeric': 'Numeric Columns',
            'stats_files': 'Number of Files',
            
            # Column Mapping
            'mapping_title': '🎯 Step 2: Map Columns',
            'mapping_auto': '💡 <strong>Auto-detection</strong>: System tried to guess column types. You can adjust manually if incorrect.',
            
            # Column Categories
            'cat_order_info': 'Order Information',
            'cat_customer_info': 'Customer Information',
            'cat_product_info': 'Product Information',
            'cat_financial': 'Financial Information',
            'cat_location': 'Location',
            'cat_sales_info': 'Sales Information',
            
            # Field Names
            'field_order_id': 'Order ID',
            'field_customer_name': 'Customer Name',
            'field_customer_id': 'Customer ID',
            'field_product_name': 'Product Name',
            'field_product_id': 'Product ID',
            'field_category': 'Category',
            'field_quantity': 'Quantity',
            'field_unit_price': 'Unit Price',
            'field_total_price': 'Total Price',
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
            
            # Analysis Button
            'analyze_button': '🚀 Proceed to Analysis',
            
            # Analysis Results
            'analysis_title': '📊 Step 3: Sales Data Analysis',
            'kpis_title': '📈 Key Results',
            'charts_title': '📊 Automatic Charts',
            'advanced_title': '🔍 Advanced Analysis',
            'correlations_title': 'Variable Correlations',
            'outliers_title': 'Outlier Detection',
            'outliers_found': 'Found {} outliers in sales',
            'no_outliers': '✅ No outliers detected in sales',
            'zero_std': 'Sales standard deviation is zero, cannot detect outliers',
            
            # Export
            'export_data': '📥 Download Modified Data (CSV)',
            'export_report': '📄 Download Full Report',
            'download_csv': '⬇️ Click to Download',
            'download_report': '⬇️ Click to Download',
            
            # Other Messages
            'loading': 'Loading...',
            'not_available': 'Not Available',
            'file_info': '📄 File Information',
            'total_rows': 'Total Rows',
            'total_columns': 'Total Columns',
            'merged_data': 'Merged Data',
            'individual_files': 'Individual Files',
        }
    }
    
    @staticmethod
    def get_translation(key, language='ar'):
        """الحصول على ترجمة المفتاح باللغة المطلوبة"""
        lang_data = SalesTranslationSystem.translations.get(language, SalesTranslationSystem.translations['ar'])
        return lang_data.get(key, key)
    
    @staticmethod
    def translate(key, **kwargs):
        """ترجمة المفتاح بناءً على اللغة الحالية"""
        language = st.session_state.get('language', 'ar')
        text = SalesTranslationSystem.get_translation(key, language)
        return text.format(**kwargs) if kwargs else text

# ==================== 5. وظائف المساعدة ====================

# تحميل CSS مع دعم متعدد اللغات
def load_sales_css(language='ar'):
    """تحميل CSS مع دعم اتجاه النص"""
    text_align = 'right' if language == 'ar' else 'left'
    font_family = "'Cairo', 'Segoe UI', Tahoma, sans-serif" if language == 'ar' else "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
    
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
        direction: {'rtl' if language == 'ar' else 'ltr'};
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
        direction: {'rtl' if language == 'ar' else 'ltr'};
    }}
    
    .file-card {{
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        font-family: {font_family};
        direction: {'rtl' if language == 'ar' else 'ltr'};
    }}
    
    .warning-box {{
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        font-family: {font_family};
        direction: {'rtl' if language == 'ar' else 'ltr'};
    }}
    
    /* تنسيق عام للصفحة */
    .stApp {{
        font-family: {font_family};
        text-align: {text_align};
    }}
    
    /* تنسيق الأزرار */
    .stButton > button {{
        border-radius: 8px;
        font-family: {font_family};
    }}
    
    /* تنسيق حقول الإدخال */
    .stSelectbox, .stTextInput, .stNumberInput {{
        font-family: {font_family};
    }}
    </style>
    
    <!-- تحميل خط Cairo للعربية -->
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
    """
    st.markdown(css, unsafe_allow_html=True)

# وظائف لتحميل الملفات المتعددة
def load_multiple_files(uploaded_files):
    """تحميل عدة ملفات Excel/CSV"""
    dataframes = []
    file_info_list = []
    
    for uploaded_file in uploaded_files:
        try:
            # تحديد نوع الملف
            file_name = uploaded_file.name.lower()
            
            if file_name.endswith('.csv'):
                # محاولة ترميزات مختلفة لملفات CSV
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
            
            # حفظ معلومات الملف
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
            st.error(f"❌ خطأ في تحميل الملف: {uploaded_file.name}: {str(e)}")
    
    return dataframes, file_info_list

def merge_dataframes(dataframes):
    """دمج عدة dataframes في dataframe واحد"""
    if not dataframes:
        return None
    
    try:
        # محاولة الدمج مع معالجة أسماء الأعمدة المختلفة
        merged_df = pd.concat(dataframes, ignore_index=True, sort=False)
        return merged_df
    except Exception as e:
        st.error(f"خطأ في دمج الملفات: {str(e)}")
        return None

# ==================== 6. تهيئة حالة الجلسة ====================

# تهيئة نظام الترجمة
translator = SalesTranslationSystem()

# إعدادات الصفحة
st.set_page_config(
    page_title="لوحة تحكم المبيعات الذكية",
    page_icon="📈",
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

# وظائف تبديل اللغة والمظهر
def toggle_language():
    st.session_state.language = 'en' if st.session_state.language == 'ar' else 'ar'
    st.rerun()

def toggle_theme():
    st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
    st.rerun()

# تحميل CSS بناءً على اللغة
load_sales_css(st.session_state.language)

# ==================== 7. الشريط الجانبي ====================

with st.sidebar:
    st.markdown(f"### {translator.translate('sidebar_settings')}")
    
    # تبديل اللغة
    current_lang = 'العربية' if st.session_state.language == 'en' else 'English'
    lang_button = st.button(f"🌐 {current_lang}", use_container_width=True)
    if lang_button:
        toggle_language()
    
    # تبديل المظهر
    current_theme = '🌙 مظلم' if st.session_state.theme == 'light' else '☀️ فاتح'
    theme_button = st.button(current_theme, use_container_width=True)
    if theme_button:
        toggle_theme()
    
    st.divider()
    
    # تحميل الإعدادات السابقة
    if st.button(translator.translate('sidebar_load_settings'), use_container_width=True):
        if os.path.exists('sales_config.json'):
            with open('sales_config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
                st.session_state.column_mapping = config.get('column_mapping', {})
                st.success(translator.translate('sidebar_load_success'))
        else:
            st.warning(translator.translate('sidebar_no_settings'))
    
    # حفظ الإعدادات
    if st.session_state.column_mapping:
        if st.button(translator.translate('sidebar_save_settings'), use_container_width=True):
            config = {
                'column_mapping': st.session_state.column_mapping,
                'saved_at': datetime.now().isoformat(),
                'language': st.session_state.language,
                'theme': st.session_state.theme
            }
            with open('sales_config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            st.success(translator.translate('sidebar_save_success'))

# ==================== 8. العنوان الرئيسي ====================

st.markdown(f"""
<div class="main-header">
    <h1>{translator.translate('main_title')}</h1>
    <p>{translator.translate('main_subtitle')}</p>
</div>
""", unsafe_allow_html=True)

# ==================== 9. تحميل الملفات المتعددة ====================

st.markdown(f"## {translator.translate('upload_title')}")

uploaded_files = st.file_uploader(
    translator.translate('upload_placeholder'),
    type=['xlsx', 'xls', 'csv'],
    help=translator.translate('upload_help'),
    accept_multiple_files=True,
    key="sales_file_uploader"
)

if uploaded_files and len(uploaded_files) > 0:
    try:
        # تحميل الملفات المتعددة
        with st.spinner(translator.translate('loading')):
            dataframes, file_info_list = load_multiple_files(uploaded_files)
        
        if dataframes and file_info_list:
            st.session_state.dataframes = dataframes
            st.session_state.file_info_list = file_info_list
            st.session_state.files_uploaded = True
            
            st.success(translator.translate('upload_success', count=len(dataframes)))
            
            # عرض معلومات الملفات
            st.markdown(f"### 📁 {translator.translate('file_info')}")
            
            for i, file_info in enumerate(file_info_list):
                with st.expander(f"{file_info['name']} ({file_info['rows']} صفوف، {file_info['columns']} أعمدة)"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("حجم الملف", f"{file_info['size']:,} بايت")
                    with col2:
                        st.metric(translator.translate('stats_records'), file_info['rows'])
                    with col3:
                        st.metric(translator.translate('stats_columns'), file_info['columns'])
                    
                    # معاينة البيانات
                    if st.checkbox(f"معاينة {file_info['name']}", key=f"preview_{i}"):
                        st.dataframe(file_info['dataframe'].head(), use_container_width=True)
            
            # خيارات دمج الملفات
            if len(dataframes) > 1:
                st.markdown("### 🔗 خيارات الدمج")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(translator.translate('merge_files'), use_container_width=True):
                        merged_df = merge_dataframes(dataframes)
                        if merged_df is not None:
                            st.session_state.merged_df = merged_df
                            st.session_state.use_merged = True
                            st.session_state.current_df = merged_df
                            st.success(translator.translate('merged_success'))
                
                with col2:
                    if st.button(translator.translate('individual_files'), use_container_width=True):
                        st.session_state.use_merged = False
                        st.session_state.current_df = dataframes[0]
                        st.info("جارٍ استخدام الملف الأول فقط")
            
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
                st.info(f"📊 **{translator.translate('merged_data')}**: {len(df_to_use)} سجل، {len(df_to_use.columns)} عمود")
            else:
                st.info(f"📊 **{translator.translate('individual_files')}**: {len(df_to_use)} سجل، {len(df_to_use.columns)} عمود")
            
            # عرض عينة من البيانات
            with st.expander(translator.translate('preview_data')):
                st.dataframe(df_to_use.head(), use_container_width=True)
            
            # عرض معلومات البيانات
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(translator.translate('stats_files'), len(dataframes))
            with col2:
                st.metric(translator.translate('stats_records'), len(df_to_use))
            with col3:
                st.metric(translator.translate('stats_columns'), len(df_to_use.columns))
            with col4:
                numeric_cols = df_to_use.select_dtypes(include=[np.number]).columns.tolist()
                st.metric(translator.translate('stats_numeric'), len(numeric_cols))
        
    except Exception as e:
        st.error(f"{translator.translate('upload_error')} {str(e)}")

# ==================== 10. تعيين أعمدة المبيعات ====================

if st.session_state.files_uploaded and st.session_state.current_df is not None:
    st.markdown(f"## {translator.translate('mapping_title')}")
    
    df = st.session_state.current_df
    columns = df.columns.tolist()
    
    # التعرف التلقائي على الأعمدة
    mapper = SalesAutoColumnMapper(df)
    auto_suggestions = mapper.auto_detect_columns()
    
    st.markdown(translator.translate('mapping_auto'), unsafe_allow_html=True)
    
    # إنشاء تخطيط تعيين الأعمدة
    column_mapping = {}
    
    # عرض تعيين الأعمدة لكل فئة
    categories = {
        translator.translate('cat_order_info'): ["order_id", "order_date", "status"],
        translator.translate('cat_customer_info'): ["customer_name", "customer_id"],
        translator.translate('cat_product_info'): ["product_name", "product_id", "category"],
        translator.translate('cat_financial'): ["quantity", "unit_price", "total_amount", "discount", "profit", "price"],
        translator.translate('cat_location'): ["region", "city", "country"],
        translator.translate('cat_sales_info'): ["salesperson", "payment_method"]
    }
    
    for category, fields in categories.items():
        st.markdown(f"### {category}")
        
        cols = st.columns(3)
        for idx, field in enumerate(fields):
            with cols[idx % 3]:
                # ترجمة اسم الحقل للعرض
                field_display = translator.translate(f'field_{field}')
                
                # اقتراح تلقائي إن وجد
                suggested_column = auto_suggestions.get(field, translator.translate('not_available'))
                
                # إنشاء selectbox
                options = [f"❌ {translator.translate('not_available')}"] + columns
                default_idx = 0
                if suggested_column in columns:
                    default_idx = columns.index(suggested_column) + 1
                
                selected = st.selectbox(
                    f"**{field_display}**",
                    options=options,
                    index=default_idx,
                    key=f"sales_map_{field}_{st.session_state.language}"
                )
                
                if selected != f"❌ {translator.translate('not_available')}":
                    column_mapping[field] = selected
    
    st.session_state.column_mapping = column_mapping
    
    # زر للمتابعة للتحليل
    if st.button(translator.translate('analyze_button'), type="primary", use_container_width=True):
        st.session_state.analysis_ready = True
        st.rerun()

# ==================== 11. التحليل الذكي للمبيعات ====================

if st.session_state.get('analysis_ready', False):
    st.markdown(f"## {translator.translate('analysis_title')}")
    
    analyzer = SalesDataAnalyzer(
        st.session_state.current_df, 
        st.session_state.column_mapping
    )
    
    # التحليل الذكي للبيانات
    with st.spinner(translator.translate('loading')):
        analysis = analyzer.analyze_all()
    
    st.session_state.analysis_results = analysis
    
    # عرض النتائج الرئيسية
    st.markdown(f"### {translator.translate('kpis_title')}")
    
    # بطاقات KPIs
    kpis = analysis.get('kpis', {})
    if kpis:
        # عرض أول 4 KPIs في صف واحد
        cols = st.columns(4)
        kpi_keys = list(kpis.keys())[:4]
        
        for idx, (col, kpi_key) in enumerate(zip(cols, kpi_keys)):
            with col:
                value = kpis[kpi_key]['value']
                label = kpis[kpi_key]['label']
                
                st.markdown(f"""
                <div class="kpi-card">
                    <div style="font-size: 2rem; margin-bottom: 10px;">
                        {kpis[kpi_key].get('icon', '📊')}
                    </div>
                    <div style="font-size: 2rem; font-weight: bold; color: #4F46E5;">
                        {value}
                    </div>
                    <div style="color: #6B7280;">
                        {label}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # عرض KPIs إضافية إذا وجدت
        if len(kpis) > 4:
            additional_kpis = list(kpis.keys())[4:8]
            if additional_kpis:
                cols = st.columns(4)
                for idx, (col, kpi_key) in enumerate(zip(cols, additional_kpis)):
                    with col:
                        value = kpis[kpi_key]['value']
                        label = kpis[kpi_key]['label']
                        
                        st.markdown(f"""
                        <div class="kpi-card">
                            <div style="font-size: 1.5rem; margin-bottom: 10px;">
                                {kpis[kpi_key].get('icon', '📊')}
                            </div>
                            <div style="font-size: 1.5rem; font-weight: bold; color: #10B981;">
                                {value}
                            </div>
                            <div style="color: #6B7280;">
                                {label}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
    
    # الرسوم البيانية الذكية
    st.markdown(f"### {translator.translate('charts_title')}")
    
    visualizer = SalesVisualizer(
        st.session_state.current_df,
        st.session_state.column_mapping,
        analysis
    )
    
    # عرض الرسوم حسب توفر البيانات
    charts = visualizer.generate_all_charts()
    
    if charts:
        # عرض الرسوم البيانية في أعمدة
        for i in range(0, len(charts), 2):
            cols = st.columns(2)
            for j in range(2):
                if i + j < len(charts):
                    chart_info = charts[i + j]
                    if chart_info['available']:
                        with cols[j]:
                            st.markdown(f"#### {chart_info['title']}")
                            st.plotly_chart(chart_info['figure'], use_container_width=True)
    else:
        st.warning("⚠️ لا توجد بيانات كافية لإنشاء الرسوم البيانية. يرجى التحقق من تعيين الأعمدة.")
    
    # تحليل إضافي
    with st.expander(translator.translate('advanced_title')):
        st.markdown(f"### {translator.translate('advanced_title')}")
        
        # تحليل العلاقات
        numeric_cols = []
        for col in st.session_state.current_df.columns:
            if pd.api.types.is_numeric_dtype(st.session_state.current_df[col]):
                numeric_cols.append(col)
        
        if len(numeric_cols) >= 2:
            st.markdown(f"#### {translator.translate('correlations_title')}")
            
            # خريطة حرارية للعلاقات
            numeric_df = st.session_state.current_df[numeric_cols]
            corr_matrix = numeric_df.corr()
            
            fig = px.imshow(
                corr_matrix,
                text_auto='.2f',
                color_continuous_scale='RdBu',
                aspect="auto",
                title=translator.translate('correlations_title')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # اكتشاف القيم الشاذة
        st.markdown(f"#### {translator.translate('outliers_title')}")
        if 'total_amount' in st.session_state.column_mapping:
            price_col = st.session_state.column_mapping['total_amount']
            if price_col in st.session_state.current_df.columns:
                try:
                    price_data = st.session_state.current_df[price_col].dropna()
                    
                    if len(price_data) > 0:
                        # حساب z-score يدويًا باستخدام numpy
                        mean_price = price_data.mean()
                        std_price = price_data.std()
                        
                        if std_price > 0:  # تجنب القسمة على صفر
                            z_scores = np.abs((price_data - mean_price) / std_price)
                            outliers_mask = z_scores > 3
                            outliers = st.session_state.current_df.loc[price_data.index[outliers_mask]]
                            
                            if len(outliers) > 0:
                                st.warning(translator.translate('outliers_found').format(len(outliers)))
                                st.dataframe(outliers[[price_col]], use_container_width=True)
                            else:
                                st.success(translator.translate('no_outliers'))
                        else:
                            st.info(translator.translate('zero_std'))
                except Exception as e:
                    st.error(f"خطأ في اكتشاف القيم الشاذة: {str(e)}")
    
    # تحميل التقارير
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        # تصدير البيانات المعدلة
        if st.button(translator.translate('export_data'), use_container_width=True):
            modified_df = analyzer.get_modified_dataframe()
            csv = modified_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label=translator.translate('download_csv'),
                data=csv,
                file_name="sales_data_modified.csv",
                mime="text/csv"
            )
    
    with col2:
        # تصدير التقرير
        if st.button(translator.translate('export_report'), use_container_width=True):
            report = analyzer.generate_report()
            st.download_button(
                label=translator.translate('download_report'),
                data=report,
                file_name="sales_analysis_report.txt",
                mime="text/plain"
            )

# ==================== 12. معلومات للمستخدمين الجدد ====================

if not st.session_state.files_uploaded:
    st.info("""
    📋 **إرشادات الاستخدام:**
    1. قم برفع ملفات Excel أو CSV تحتوي على بيانات مبيعات
    2. سيقوم النظام بالتعرف التلقائي على أعمدة البيانات
    3. يمكنك تعديل تعيين الأعمدة يدوياً إذا لزم الأمر
    4. انتقل إلى التحليل للحصول على نتائج ورسوم بيانية
    5. يمكنك تحميل البيانات المعدلة والتقارير
    
    💡 **نصائح:**
    - يمكنك رفع ملفات متعددة ودمجها في ملف واحد
    - تحقق من تعيين الأعمدة قبل التحليل
    - استخدم زر حفظ الإعدادات لحفظ التكوين
    """)