from app import calculate_bmi, transform_height, bmi_category, category_health_risk, process_bmi_list, \
    calculate_total_overweight_count


def test_transform_height():
    height = 175
    height_meters = 1.75
    expected_height = transform_height(height=height)
    assert expected_height == height_meters


def test_calculate_bmi():
    weight = 75
    height = 1.75
    expected_bmi = 24.49
    calculated_bmi = calculate_bmi(mass=weight, height=height)
    assert expected_bmi == calculated_bmi


def test_bmi_category():
    bmi = 24.49
    expected_category = "normal"
    calculated_category = bmi_category(bmi=bmi)
    assert expected_category == calculated_category


def test_bmi_category_precision():
    bmi = 24.94
    expected_category = "normal"
    calculated_category = bmi_category(bmi=bmi)
    assert expected_category == calculated_category


def test_health_risk():
    category = "normal"
    expected_health = "low risk"
    calculated_risk = category_health_risk(category=category)
    assert expected_health == calculated_risk


def test_process_bmi_list():
    input_json_dict = {'list': [{'Gender': 'Male', 'HeightCm': 171, 'WeightKg': 96},
                                {'Gender': 'Male', 'HeightCm': 161, 'WeightKg': 85},
                                {'Gender': 'Male', 'HeightCm': 180, 'WeightKg': 77},
                                {'Gender': 'Female', 'HeightCm': 166, 'WeightKg': 62},
                                {'Gender': 'Female', 'HeightCm': 150, 'WeightKg': 70},
                                {'Gender': 'Female', 'HeightCm': 167, 'WeightKg': 82}]}

    expected_json_dict = {'list': [
        {'Gender': 'Male', 'HeightCm': 171, 'WeightKg': 96, 'Bmi': 32.83, 'BmiCategory': 'mildly_obese',
         'HealthRisk': 'medium risk'},
        {'Gender': 'Male', 'HeightCm': 161, 'WeightKg': 85, 'Bmi': 32.79, 'BmiCategory': 'mildly_obese',
         'HealthRisk': 'medium risk'},
        {'Gender': 'Male', 'HeightCm': 180, 'WeightKg': 77, 'Bmi': 23.77, 'BmiCategory': 'normal',
         'HealthRisk': 'low risk'},
        {'Gender': 'Female', 'HeightCm': 166, 'WeightKg': 62, 'Bmi': 22.5, 'BmiCategory': 'normal',
         'HealthRisk': 'low risk'},
        {'Gender': 'Female', 'HeightCm': 150, 'WeightKg': 70, 'Bmi': 31.11, 'BmiCategory': 'mildly_obese',
         'HealthRisk': 'medium risk'},
        {'Gender': 'Female', 'HeightCm': 167, 'WeightKg': 82, 'Bmi': 29.4, 'BmiCategory': 'over_weight',
         'HealthRisk': 'enhanced risk'}]}

    processed_list = process_bmi_list(input_json_dict.get("list"))
    assert expected_json_dict == processed_list


def test_calculate_total_overweight_count():
    input_json_dict = {
        "list": [
            {
                "Bmi": 23.77,
                "BmiCategory": "normal",
                "HealthRisk": "low risk",
                "Gender": "Male",
                "HeightCm": 180,
                "WeightKg": 77.0
            },
            {
                "Bmi": 22.5,
                "BmiCategory": "normal",
                "HealthRisk": "low risk",
                "Gender": "Female",
                "HeightCm": 166,
                "WeightKg": 62.0
            },
            {
                "Bmi": 31.11,
                "BmiCategory": "mildly_obese",
                "HealthRisk": "medium risk",
                "Gender": "Female",
                "HeightCm": 150,
                "WeightKg": 70.0
            },
            {
                "Bmi": 29.4,
                "BmiCategory": "over_weight",
                "HealthRisk": "enhanced risk",
                "Gender": "Female",
                "HeightCm": 167,
                "WeightKg": 82.0
            }
        ]
    }

    expected_total_count = dict(total_count=1)
    calculate_total_over_weight = calculate_total_overweight_count(input_json_dict.get("list"))
    assert expected_total_count == calculate_total_over_weight
