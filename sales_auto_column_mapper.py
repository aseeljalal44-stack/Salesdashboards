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
            'cost': {
                'patterns': ['cost', 'تكلفة', 'التكلفة'],
                'keywords': ['cost', 'تكلفة']
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