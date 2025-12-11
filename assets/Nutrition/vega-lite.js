vega_lite_script = {
    "$schema": "https://vega.github.io/schema/vega-lite/v6.json",
    "data": {"name": "jsData"},
    "padding": 30,
    "spacing": 100,
    "params": [
        {"name": "selected_food", "value": "swiss cheese"},
        {"name": "h1", "value": false},
        {"name": "h2", "value": false},
        {"name": "h3", "value": false},
        {"name": "h4", "value": false},
        {"name": "h5", "value": false},
        {
            "name": "focused_category",
            "expr": "if(h1, 1, if(h2, 2, if(h3, 3, if(h4, 4, if(h5, 5, 0)))))"
        }
    ],
    "hconcat": [
        {
            "transform": [
                {"fold": ["calories", "carbs", "protein", "sugar", "fat"], "as": ["category", "value"]},
                {
                    "calculate": "datum.category == 'calories' ? 'Calories' : datum.category == 'carbs' ? 'Carbs (grams)' : datum.category == 'protein' ? 'Protein (grams)' : datum.category == 'sugar' ? 'Sugar (grams)' : 'Fats (grams)'", "as": "unit_category"
                }
            ],
            "layer": [
                {
                    "title": {"text": "Selected Foods Nutrients Bar Chart", "anchor": "middle", "fontSize": 22},
                    "width": 500,
                    "height": 500,
                    "mark": {"type": "bar", "tooltip": true},
                    "encoding": {
                        "x": {"field": "unit_category", "type": "nominal", "axis": {"labelAngle": 0}, "title": "Nutrient Category"},
                        "y": {"field": "value", "aggregate": "sum", "type": "quantitative", "title": "Total Nutrient Value"}
                    }
                }
            ]
        },
        {
            "title": {"text": "Individual Food Nutrient Impact Charts", "anchor": "middle", "fontSize": 22},
            "center": true,
            "spacing": 0,
            "vconcat":[
                {
                    "transform": [
                        {"joinaggregate": [{"op": "sum", "field": "calories", "as": "calories_sum"}]},
                        {"calculate": "datum.food === selected_food ? 'Food Selected' : 'Other Foods'", "as": "category"}
                    ],
                    "layer": [
                        {
                            "width": 150,
                            "height": 150,
                            "mark": {"type": "arc", "innerRadius": 50, "tooltip": true},
                            "encoding": {
                                "theta": {"field": "calories", "aggregate": "sum", "type": "quantitative"},
                                "color": {"field": "category", "type": "nominal", "legend": null, "scale": {"range": ["#4c78a8", "#193340"]}},
                            }
                        },
                        {
                            "transform": [
                                {"filter": "datum.food === selected_food"},
                                {"calculate": "datum.calories / datum.calories_sum", "as": "percentage"}
                            ],
                            "mark": {"type": "text", "fontSize": 22},
                            "encoding": {
                                "text": {"value": "Calories"},
                                "tooltip": {"field": "percentage", "type": "quantitative", "title": "Percentage", "format": ".2%"}
                            }
                        }
                    ]
                },
                {
                    "spacing": 160,
                    "hconcat": [
                        {
                            "transform": [
                                {"joinaggregate": [{"op": "sum", "field": "carbs", "as": "carbs_sum"}]},
                                {"calculate": "datum.food === selected_food ? 'Food Selected' : 'Other Foods'", "as": "category"}
                            ],
                            "layer": [
                                {
                                    "width": 150,
                                    "height": 150,
                                    "mark": {"type": "arc", "innerRadius": 50, "tooltip": true},
                                    "encoding": {
                                        "theta": {"field": "carbs", "aggregate": "sum", "type": "quantitative"},
                                        "color": {"field": "category", "type": "nominal", "legend": null, "scale": {"range": ["#4c78a8", "#193340"]}},
                                    }
                                },
                                {
                                    "transform": [
                                        {"filter": "datum.food === selected_food"},
                                        {"calculate": "datum.carbs / datum.carbs_sum", "as": "percentage"}
                                    ],
                                    "mark": {"type": "text", "fontSize": 22},
                                    "encoding": {
                                        "text": {"value": "Carbs"},
                                        "tooltip": {"field": "percentage", "type": "quantitative", "title": "Percentage", "format": ".2%"}
                                    }
                                }
                            ]
                        },
                        {
                            "transform": [
                                {"joinaggregate": [{"op": "sum", "field": "protein", "as": "protein_sum"}]},
                                {"calculate": "datum.food === selected_food ? 'Food Selected' : 'Other Foods'", "as": "category"}
                            ],
                            "layer": [
                                {
                                    "width": 150,
                                    "height": 150,
                                    "mark": {"type": "arc", "innerRadius": 50, "tooltip": true},
                                    "encoding": {
                                        "theta": {"field": "protein", "aggregate": "sum", "type": "quantitative"},
                                        "color": {"field": "category", "type": "nominal", "legend": null, "scale": {"range": ["#4c78a8", "#193340"]}},
                                    }
                                },
                                {
                                    "transform": [
                                        {"filter": "datum.food === selected_food"},
                                        {"calculate": "datum.protein / datum.protein_sum", "as": "percentage"}
                                    ],
                                    "mark": {"type": "text", "fontSize": 22},
                                    "encoding": {
                                        "text": {"value": "Proteins"},
                                        "tooltip": {"field": "percentage", "type": "quantitative", "title": "Percentage", "format": ".2%"}
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "spacing": 30,
                    "hconcat": [
                        {
                            "transform": [
                                {"joinaggregate": [{"op": "sum", "field": "fat", "as": "fat_sum"}]},
                                {"calculate": "datum.food === selected_food ? 'Food Selected' : 'Other Foods'", "as": "category"}
                            ],
                            "layer": [
                                {
                                    "width": 150,
                                    "height": 150,
                                    "mark": {"type": "arc", "innerRadius": 50, "tooltip": true},
                                    "encoding": {
                                        "theta": {"field": "fat", "aggregate": "sum", "type": "quantitative"},
                                        "color": {"field": "category", "type": "nominal", "legend": null, "scale": {"range": ["#4c78a8", "#193340"]}},
                                    }
                                },
                                {
                                    "transform": [
                                        {"filter": "datum.food === selected_food"},
                                        {"calculate": "datum.fat / datum.fat_sum", "as": "percentage"}
                                    ],
                                    "mark": {"type": "text", "fontSize": 22},
                                    "encoding": {
                                        "text": {"value": "Fats"},
                                        "tooltip": {"field": "percentage", "type": "quantitative", "title": "Percentage", "format": ".2%"}
                                    }
                                }
                            ]
                        },
                        {
                            "transform": [
                                {"joinaggregate": [{"op": "sum", "field": "sugar", "as": "sugar_sum"}]},
                                {"calculate": "datum.food === selected_food ? 'Food Selected' : 'Other Foods'", "as": "category"}
                            ],
                            "layer": [
                                {
                                    "width": 150,
                                    "height": 150,
                                    "mark": {"type": "arc", "innerRadius": 50, "tooltip": true},
                                    "encoding": {
                                        "theta": {"field": "sugar", "aggregate": "sum", "type": "quantitative"},
                                        "color": {"field": "category", "type": "nominal", "legend": null, "scale": {"range": ["#4c78a8", "#193340"]}},
                                    }
                                },
                                {
                                    "transform": [
                                        {"filter": "datum.food === selected_food"},
                                        {"calculate": "datum.sugar / datum.sugar_sum", "as": "percentage"}
                                    ],
                                    "mark": {"type": "text", "fontSize": 22},
                                    "encoding": {
                                        "text": {"value": "Sugars"},
                                        "tooltip": {"field": "percentage", "type": "quantitative", "title": "Percentage", "format": ".2%"}
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]
}

var vis_view;

vegaEmbed('#vis2', vega_lite_script).then(result => {
    vis_view = result.view;
    autocompleteV4();
}).catch(console.error);

function updateVis() {
    const selected_data = [];
    const selected_food = document.getElementById("food-selectV4").value;

    for(const row of document.getElementById("TableV4").getElementsByClassName("selected-tableV4-row")) {
        const count = row.children[1].firstChild.value;
        const datum = Object.assign({}, data.find(d => d.food === row.firstChild.textContent));

        for (const k in datum) {
            if (typeof(datum[k]) !== "string") {
                datum[k] *= count;
            }
        }

        selected_data.push(datum);
    }

    vis_view.change("jsData", vega.changeset().remove(vega.truthy).insert(selected_data)).signal("selected_food", selected_food).run();
}