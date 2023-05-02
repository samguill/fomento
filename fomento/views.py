from django.db.models import Sum
from drf_excel.mixins import XLSXFileMixin
from drf_excel.renderers import XLSXRenderer
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from django.http import JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from customer.models import Position, WorkPeriodCustomer
from company.models import Company
from employee.models import EmployeeTime
from employee.api.serializers import EmployeeTimeHourlyReportDetailSerializer, EmployeeTimeHourlyReportSerializer, \
    EmployeeTimePayrollReportSerializer

from personal.utils import get_from_dict, render_to_pdf
import json


class FomentoViewReport(XLSXFileMixin, ReadOnlyModelViewSet):
    serializer_class = EmployeeTimeHourlyReportSerializer
    renderer_classes = [XLSXRenderer, ]
    filename = 'position_report.xlsx'

    xlsx_custom_cols = {
        'description': {
            'label': 'Position Description'
        },
        'total_sum': {
            'label': 'Total Amount'
        }
    }

    column_header = {
        'column_width': [35, 25],
        'height': 35,
        'style': {
            'fill': {
                'fill_type': 'solid',
                'start_color': 'FF21ADB4',
            },
            'alignment': {
                'horizontal': 'center',
                'vertical': 'center',
                'wrapText': True,
                'shrink_to_fit': True,
            },
            'border_side': {
                'border_style': 'medium',
                'color': 'FF000000',
            },
            'font': {
                'name': 'Arial',
                'size': 14,
                'bold': True,
                'color': 'FF000000',
            },
        },
    }
    body = {
        'style': {
            'fill': {
                'fill_type': 'solid',
                'start_color': 'FFFFFFFF',
            },
            'alignment': {
                'horizontal': 'center',
                'vertical': 'center',
                'wrapText': True,
                'shrink_to_fit': True,
            },
            'border_side': {
                'border_style': 'thin',
                'color': 'FF000000',
            },
            'font': {
                'name': 'Arial',
                'size': 14,
                'bold': False,
                'color': 'FF000000',
            }
        },
        'height': 30,
    }
    column_data_styles = {
        'distance': {
            'alignment': {
                'horizontal': 'right',
                'vertical': 'top',
            },
            'format': '0.00E+00'
        },
        'created_at': {
            'format': 'd.m.y h:mm',
        }
    }

    def get_renderers(self):
        format = get_from_dict(
            dictionary=self.request.query_params,
            key="format",
            default_if_not_exist=1,
            default_if_empty=1,
            cast_function=str
        )

        if format == "json":
            return [JSONRenderer(),]

        return [XLSXRenderer(), ]

    def get_queryset(self):
        queryset = Position.objects.all()

        company = get_from_dict(
            dictionary=self.request.query_params,
            key="company",
            default_if_not_exist=1,
            default_if_empty=1,
            cast_function=int
        )

        work_period = get_from_dict(
            dictionary=self.request.query_params,
            key="work_period",
            default_if_not_exist=1,
            default_if_empty=1,
            cast_function=int
        )

        work_customer = get_from_dict(
            dictionary=self.request.query_params,
            key="work_customer",
            default_if_not_exist=1,
            default_if_empty=1,
            cast_function=int
        )

        queryset = queryset.filter(employeetime__company=company, employeetime__work_customer__id=work_customer,
                                   employeetime__work_period=work_period)
        queryset = queryset.annotate(total_sum=Sum('employeetime__total')).order_by('total_sum')
        return queryset

    def get_sheet_view_options(self):
        return {
            'rightToLeft': False,
            'showGridLines': False
        }

    def get_header(self):
        work_customer = self.request.query_params.get('work_period')
        wpc = WorkPeriodCustomer.objects.get(id=int(work_customer))
        return {
            'tab_title': 'Position - Summary',  # title of tab/workbook
            'use_header': True,  # show the header_title
            'header_title': f'Hourly by Position - Summary\n'
                            f'{wpc}',
            'height': 95,
            'column_width': [100],
            # 'img': 'app/images/MyLogo.png',
            'style': {
                'fill': {
                    'fill_type': 'solid',
                    'start_color': 'FFFFFFFF',
                },
                'alignment': {
                    'horizontal': 'center',
                    'vertical': 'center',
                    'wrapText': True,
                    'shrink_to_fit': True,
                },
                'border_side': {
                    'border_style': 'thin',
                    'color': 'FF000000',
                },
                'font': {
                    'name': 'Arial',
                    'size': 16,
                    'bold': True,
                    'color': 'FF000000',
                }
            }
        }

    def __get_report_data(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.get_queryset(), many=True)
        serializer.is_valid()
        serializer.save()
        return Response({"results": serializer.data})

    @action(detail=False, methods=['POST'], url_path='report')
    def report(self, request, *args, **kwargs):
        return self.__get_report_data(request)

    def __get_report_data_pdf(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.get_queryset(), many=True)
        serializer.is_valid()
        serializer.save()
        return serializer.data

    @action(detail=False, methods=['POST'], url_path='report-pdf')
    def report_detail_pdf(self, request, *args, **kwargs):
        context = {}
        data = self.__get_report_data_pdf(request)
        # call rendering pdf function
        work_customer = self.request.query_params.get('work_customer')
        title = WorkPeriodCustomer.objects.get(id=int(work_customer))
        template = "reports/position/summary-pdf.html"
        context["results"] = data

        # f'Hourly by Position - Detail\n{title}'
        context["title"] = title
        pdf = render_to_pdf(template, context)
        return pdf





