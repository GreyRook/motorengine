#!/usr/bin/env python
# -*- coding: utf-8 -*-

from decimal import Decimal

from preggy import expect
import mongoengine
from tornado.testing import gen_test

import motorengine
from tests.integration.base import BaseIntegrationTest

COLLECTION = 'IntegrationTestDecimalField'


class MongoDocument(mongoengine.Document):
    meta = {'collection': COLLECTION}
    number = mongoengine.DecimalField()


class MotorDocument(motorengine.Document):
    __collection__ = COLLECTION
    number = motorengine.DecimalField()


class TestIntField(BaseIntegrationTest):
    @gen_test
    def test_can_integrate(self):
        mongo_document = MongoDocument(number=Decimal("10.53")).save()

        result = yield MotorDocument.objects.get(mongo_document.id)

        expect(result._id).to_equal(mongo_document.id)
        expect(result.number).to_equal(mongo_document.number)

    @gen_test
    def test_can_integrate_backwards(self):
        motor_document = yield MotorDocument.objects.create(number=Decimal("10.53"))

        result = MongoDocument.objects.get(id=motor_document._id)

        expect(result.id).to_equal(motor_document._id)
        expect(result.number).to_equal(motor_document.number)
