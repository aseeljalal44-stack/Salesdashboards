"""
وحدة إنشاء الرسوم البيانية الذكية للمبيعات
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

class SalesSmartVisualizer:
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