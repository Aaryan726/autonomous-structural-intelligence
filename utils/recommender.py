def recommend_materials(detection_summary):
    rooms_detected = detection_summary.get("rooms_detected", 0)
    wall_segments = detection_summary.get("wall_segments", 0)
    total_area = detection_summary.get("total_area", 0.0)
    recommendations = []

    if wall_segments > 5:
        recommendations.append({
            "component": "Exterior Walls",
            "material": "Brick",
            "reason": "Durability, thermal insulation, and cost-effective.",
            "properties": "Strong, durable, good insulation"
        })
    else:
        recommendations.append({
            "component": "Walls",
            "material": "Concrete Blocks",
            "reason": "Faster construction and good strength.",
            "properties": "Fast construction, solid, cost-effective"
        })

    recommendations.append({
        "component": "Floor Slabs",
        "material": "Reinforced Concrete",
        "reason": "High load bearing capacity and fire resistance.",
        "properties": "High strength, fire resistant"
    })

    if rooms_detected > 3:
        recommendations.append({
            "component": "Structure Frame",
            "material": "Steel Frame",
            "reason": "Spans large areas, supports multiple floors.",
            "properties": "Flexible design, strong, suitable for multi-floor"
        })
    else:
        recommendations.append({
            "component": "Structure Frame",
            "material": "Timber Frame",
            "reason": "Lighter load, eco-friendly, and cost-effective.",
            "properties": "Sustainable, light weight, cost saving"
        })

    recommendations.append({
        "component": "Windows",
        "material": "Tempered Glass",
        "reason": "Safety, natural lighting, and ventilation.",
        "properties": "Safe, lets in light, strong"
    })

    if total_area > 10000:
        recommendations.append({
            "component": "Foundation",
            "material": "High-Strength Concrete",
            "reason": "Large building, needs deep and strong foundation.",
            "properties": "Heavy-duty, high strength"
        })
    else:
        recommendations.append({
            "component": "Foundation",
            "material": "Plain Cement Concrete",
            "reason": "Sufficient for smaller structures.",
            "properties": "Standard foundation, cost effective"
        })

    recommendations.append({
        "component": "Roof",
        "material": "Clay Tiles or Metal Roofing",
        "reason": "Weather resistant and long lifespan.",
        "properties": "Durable, weather-proof"
    })

    return recommendations


def get_material_color(material):
    color_map = {
        "Brick": "#B22222",
        "Concrete Blocks": "#A9A9A9",
        "Reinforced Concrete": "#666666",
        "Steel Frame": "#4682B4",
        "Timber Frame": "#8B5C2D",
        "Tempered Glass": "#87CEEB",
        "High-Strength Concrete": "#4D4D4D",
        "Plain Cement Concrete": "#C0C0C0",
        "Clay Tiles or Metal Roofing": "#DAA520",
    }
    return color_map.get(material, "#CCCCCC")