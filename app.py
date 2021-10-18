from multiprocessing import Pool

from flask import Flask, request
from flask_restx import Api, Resource, fields, abort

app = Flask(__name__)
api = Api(app, title="BMI App", version="1.1")

if __name__ == "main":
    app.run()

HEALTH_RISK = "unknown", \
              "malnutrition", \
              "low risk", \
              "enhanced risk", \
              "medium risk", \
              "high risk", \
              "very high risk"

CATEGORIES = "unknown", \
             "under_weight", \
             "normal", \
             "over_weight", \
             "mildly_obese", \
             "slightly_obese", \
             "very_obese",

CATEGORIES_MAP_HEALTH_RISK = {category: risk for category, risk in zip(CATEGORIES, HEALTH_RISK)}

'''
The BMI (Body Mass Index) in (kg/m2 ) is equal to the weight in kilograms (kg) divided
by your height in meters squared (m)2 .
'''

'''
mass in KG
height in meters
'''


def calculate_bmi(mass, height):
    return round(mass / (height ** 2), 2)


def transform_height(height):
    return height / 100


def bmi_category(bmi):
    category = CATEGORIES[0]
    bmi = round(bmi, 1)
    if bmi <= 18.4:
        category = CATEGORIES[1]
    elif 18.5 <= bmi <= 24.9:
        category = CATEGORIES[2]
    elif 25.0 <= bmi <= 29.9:
        category = CATEGORIES[3]
    elif 30.0 <= bmi <= 34.9:
        category = CATEGORIES[4]
    elif 35.0 <= bmi <= 39.9:
        category = CATEGORIES[5]
    elif bmi >= 40.0:
        category = CATEGORIES[6]
    return category


def category_health_risk(category):
    return CATEGORIES_MAP_HEALTH_RISK[category]


ns = api.namespace(name="bmi", description="BMI apis")
# take care of
bmi_request_model = ns.model(name="BmiRequestModel",
                             model=dict(
                                 Gender=fields.String(enum=("Male", "Female"), required=True),
                                 HeightCm=fields.Integer(min=0, required=True),
                                 WeightKg=fields.Float(decimals=1, min=0.0, default=0.0)
                             )
                             )
bmi_response_model = ns.inherit("BmiResponseModel", bmi_request_model, dict(
    Bmi=fields.Float(decimals=2, min=0.0, default=0.0),
    BmiCategory=fields.String(enum=CATEGORIES, default=CATEGORIES[0]),
    HealthRisk=fields.String(enum=HEALTH_RISK, default=HEALTH_RISK[0])
))


def process_bmi(input_dict):
    bmi = calculate_bmi(mass=input_dict["WeightKg"], height=transform_height(input_dict["HeightCm"]))
    category = bmi_category(bmi)
    risk = category_health_risk(category)
    input_dict.update(dict(
        Bmi=bmi,
        BmiCategory=category,
        HealthRisk=risk
    ))
    return input_dict


bmi_list_request_model = ns.model("BmiListRequestModel", dict(list=fields.List(fields.Nested(bmi_request_model))))
bmi_list_response_model = ns.model("BmiListResponseModel", dict(list=fields.List(fields.Nested(bmi_response_model))))


@ns.route("")
class BmiHandler(Resource):
    @ns.expect(bmi_request_model, validate=True)
    @ns.marshal_with(bmi_response_model)
    def post(self):
        return process_bmi(request.get_json())


def process_bmi_list(input_json_list):
    with Pool() as p:
        processed_list = p.map(process_bmi, input_json_list)
    return dict(list=processed_list)


@ns.route("/list")
class BmiListHandler(Resource):
    @ns.expect(bmi_list_request_model)
    @ns.marshal_with(bmi_list_response_model)
    def post(self):
        input_json_list = request.get_json().get("list")
        if input_json_list:
            return process_bmi_list(input_json_list=input_json_list)
        else:
            abort(400, "no input was provided")


def filter_overweight(input_json):
    return input_json.get("BmiCategory") == CATEGORIES[3]


def calculate_total_overweight_count(input_json_list):
    processed_list = list(filter(filter_overweight, input_json_list))
    return dict(total_count=len(processed_list))


total_count_request_model = ns.clone("TotalCountRequestModel", bmi_list_response_model)
total_count_response_model = ns.model("TotalCountResponseModel", dict(total_count=fields.Integer()))


@ns.route("/list/overweight")
class TotalOverWeight(Resource):
    @ns.expect(total_count_request_model)
    @ns.marshal_with(total_count_response_model)
    def post(self):
        input_json_list = request.get_json().get("list")
        if input_json_list:
            return calculate_total_overweight_count(input_json_list)
        else:
            abort(400, "no input was provided")
