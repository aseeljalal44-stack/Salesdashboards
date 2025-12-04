"""
وحدة التعرف التلقائي على أعمدة بيانات المبيعات
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime

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