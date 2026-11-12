
import pytest
from irrigation_scheduler import should_irrigate, water_volume, schedule


# ==========================================
# 1. SHOULD_IRRIGATE() TEST CASES
# ==========================================

def test_wet_soil_no_irrigation():
    assert should_irrigate(70, 0, "seedling") is False


def test_rainfall_high_no_irrigation():
    assert should_irrigate(40, 10, "seedling") is False


def test_seedling_low_moisture():
    assert should_irrigate(30, 0, "seedling") is True


def test_seedling_boundary_moisture():
    assert should_irrigate(45, 0, "seedling") is False


def test_seedling_moisture_below_limit():
    assert should_irrigate(44, 0, "seedling") is True


def test_flowering_low_moisture():
    assert should_irrigate(40, 0, "flowering") is True


def test_flowering_high_moisture():
    assert should_irrigate(55, 0, "flowering") is False


def test_flowering_boundary():
    assert should_irrigate(54, 0, "flowering") is True


def test_other_stage_low_rainfall():
    assert should_irrigate(30, 2, "mature") is True


def test_other_stage_rainfall_boundary():
    assert should_irrigate(30, 5, "mature") is False


def test_other_stage_high_rainfall():
    assert should_irrigate(30, 7, "mature") is False


def test_other_stage_sufficient_moisture():
    assert should_irrigate(40, 0, "mature") is False


def test_moisture_boundary_60():
    assert should_irrigate(60, 0, "seedling") is False


# ==========================================
# 2. WATER_VOLUME() TEST CASES
# ==========================================

def test_seedling_volume():
    assert water_volume(10, "seedling", 20) == 20


def test_flowering_volume():
    assert water_volume(10, "flowering", 20) == 50


def test_other_stage_volume():
    assert water_volume(10, "mature", 20) == 40


def test_high_temperature():
    assert water_volume(10, "seedling", 40) == 30


def test_low_temperature():
    assert water_volume(10, "seedling", 5) == 10


def test_temperature_boundary_high():
    assert water_volume(10, "seedling", 35) == 20


def test_temperature_boundary_low():
    assert water_volume(10, "seedling", 10) == 20


def test_invalid_zero_area():
    with pytest.raises(ValueError):
        water_volume(0, "seedling", 20)


def test_invalid_negative_area():
    with pytest.raises(ValueError):
        water_volume(-5, "seedling", 20)


def test_fractional_area():
    assert water_volume(2.5, "seedling", 20) == 5


# ==========================================
# 3. SCHEDULE() TEST CASES
# ==========================================

def test_schedule_irrigates_zone():
    zones = [
        ("Zone A", 10, 30, 0, "seedling", 20)
    ]
    assert schedule(zones, 100) == ["Zone A"]


def test_schedule_skips_wet_zone():
    zones = [
        ("Zone A", 10, 70, 0, "seedling", 20)
    ]
    assert schedule(zones, 100) == []


def test_schedule_insufficient_budget():
    zones = [
        ("Zone A", 10, 30, 0, "seedling", 20)
    ]
    assert schedule(zones, 10) == []


def test_schedule_multiple_zones():
    zones = [
        ("Zone A", 10, 30, 0, "seedling", 20),
        ("Zone B", 5, 30, 0, "seedling", 20)
    ]
    assert schedule(zones, 100) == ["Zone A", "Zone B"]


def test_schedule_budget_exhausted():
    zones = [
        ("Zone A", 10, 30, 0, "seedling", 20),
        ("Zone B", 10, 30, 0, "seedling", 20)
    ]
    assert schedule(zones, 25) == ["Zone A"]


def test_schedule_skips_zone_and_continues():
    zones = [
        ("Zone A", 10, 70, 0, "seedling", 20),
        ("Zone B", 5, 30, 0, "seedling", 20)
    ]
    assert schedule(zones, 100) == ["Zone B"]


def test_schedule_empty_zones():
    assert schedule([], 100) == []


def test_schedule_exact_budget():
    zones = [
        ("Zone A", 10, 30, 0, "seedling", 20)
    ]
    assert schedule(zones, 20) == ["Zone A"]
