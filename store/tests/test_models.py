
from store.models import Customer, Brand
import pytest


class TestCustomerModel(object):
    """Test case for Customer Model"""

    def test_field_value(self, create_customer):
        new_customer, client = create_customer(username='nana')
        assert new_customer.user.username == 'nana'
        assert str(new_customer) == 'nana'
        assert new_customer.age == 23




class TestBrandModel(object):
    """Test case for Brand Model"""

    def test_field_value(self, create_brand):
        new_brand = create_brand(username='sasa', brand='bikaji')
        brand_view = Brand.objects.all()
        print('Brand', brand_view.values())
        assert new_brand.user.username == 'sasa'
        assert str(new_brand) == 'bikaji'
        assert new_brand.brand == 'bikaji'
