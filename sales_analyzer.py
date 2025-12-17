"""
وحدة التحليل الذكي لبيانات المبيعات
"""

import pandas as pd
import numpy as np
from datetime import datetime

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
                    
 # هامش الربح (Profit Margin) — الحساب الصحيح
if 'total_amount' in self.mapping and 'profit' in self.mapping:
    amount_col = self.mapping['total_amount']
    profit_col = self.mapping['profit']

    if amount_col in self.df.columns and profit_col in self.df.columns:
        try:
            total_sales = pd.to_numeric(self.df[amount_col], errors='coerce').sum()
            total_profit = pd.to_numeric(self.df[profit_col], errors='coerce').sum()

            if total_sales > 0:
                profit_margin = (total_profit / total_sales) * 100
            else:
                profit_margin = 0

            kpis['profit_margin'] = {
                'value': f"{profit_margin:.2f}%",
                'label': 'هامش الربح',
                'icon': '⚖️'
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
