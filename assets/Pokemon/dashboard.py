import pandas as pd
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
import threading
import time
 
# Check if the unified dashboard.html exists
dashboard_path = Path(__file__).parent / "dashboard.html"
if not dashboard_path.exists():
    print(f"Error: dashboard.html not found!")
    print("Please ensure dashboard.html is in the same directory as this script.")
    exit(1)

csv_path = Path(__file__).parent / "pokemon.csv"
if not csv_path.exists():
    print(f"Error: pokemon CSV not found!")
    print("Please place your pokemon CSV file in the same directory as this script.")
    exit(1)

df = pd.read_csv(csv_path)

icons_dir = Path(__file__).parent / "Pokémon Icons"

data_json = df.to_json(orient='records')


def create_generation_page():
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pokémon Types by Generation</title>
    <script src="https://cdn.jsdelivr.net/npm/vega@5"></script>
    <script src="https://cdn.jsdelivr.net/npm/vega-lite@6"></script>
    <script src="https://cdn.jsdelivr.net/npm/vega-embed@6"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #3B4CCA 0%, #FF0000 100%);
            min-height: 100vh;
            padding: 0 20px 40px 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .pie-chart-section {{
            background: white;
            padding: 60px 40px;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            margin-top: 100px;
        }}
        
        .section-title {{
            font-size: 28px;
            font-weight: bold;
            color: #333;
            margin-bottom: 30px;
            text-align: center;
        }}
        
        .generation-selector {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }}
        
        .generation-selector label {{
            font-size: 16px;
            font-weight: 600;
            color: #333;
        }}
        
        .generation-selector select {{
            padding: 12px 20px;
            font-size: 16px;
            border: 2px solid #667eea;
            border-radius: 8px;
            background-color: white;
            color: #333;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
        }}
        
        .generation-selector select:hover {{
            border-color: #764ba2;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
        }}
        
        .generation-selector select:focus {{
            outline: none;
            border-color: #764ba2;
            box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
        }}
        
        #pieChart {{
            width: 100%;
            display: flex;
            justify-content: center;
        }}
        
        .generation-count {{
            text-align: center;
            margin-top: 20px;
            font-size: 18px;
            font-weight: 600;
            color: #667eea;
        }}
    </style>
</head>
<body>
    <nav style="position: sticky; top: 0; background: white; padding: 15px 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); z-index: 1000; margin: 0; width: 100vw; margin-left: calc(-50vw + 50%);">
        <a href="./index.html" style="margin-left: 20px;">PokéSearch</a>
        <a href="./generation.html" style="margin-left: 20px;">Generation PokéTypes</a>
        <a href="./final.html#pokemon-comparison" style="margin-left: 20px;">PokéCompare</a>
        <a href="./final.html" style="margin-left: 20px;">Average PokéStats</a>
        <a href="./final.html#pokemon-scatter" style="margin-left: 20px;">PokéScatter</a>
    </nav>

    <div class="container">
        <div class="pie-chart-section">
            <div class="section-title">Pokémon Types by Generation</div>
            
            <div class="generation-selector">
                <label for="generationSelect">Select Generation:</label>
                <select id="generationSelect">
                    <option value="">-- Choose a generation --</option>
                </select>
            </div>
            
            <div id="pieChart"></div>
            <div id="generationCount" class="generation-count" style="display: none;"></div>
            <div id="noPieSelection" style="text-align: center; color: #999; padding: 40px 20px; display: block;">
                Select a generation to view type distribution
            </div>
        </div>
    </div>

    <script>
        const rawData = {data_json};
        
        function initializeGenerationDropdown() {{
            const generationSelect = document.getElementById('generationSelect');
            const generations = [...new Set(rawData.map(p => p.Generation))].sort((a, b) => a - b);
            
            generations.forEach(gen => {{
                const option = document.createElement('option');
                option.value = gen;
                option.textContent = 'Generation ' + gen;
                generationSelect.appendChild(option);
            }});
            
            generationSelect.addEventListener('change', function() {{
                if (this.value) {{
                    createPieChart(parseInt(this.value));
                }} else {{
                    document.getElementById('pieChart').innerHTML = '';
                    document.getElementById('noPieSelection').style.display = 'block';
                }}
            }});
        }}
        
        function createPieChart(generation) {{
            const generationData = rawData.filter(p => p.Generation === generation);
            
            const typeCount = {{}};
            generationData.forEach(pokemon => {{
                const type1 = pokemon['Type 1'] || 'Unknown';
                typeCount[type1] = (typeCount[type1] || 0) + 1;
                
                if (pokemon['Type 2']) {{
                    typeCount[pokemon['Type 2']] = (typeCount[pokemon['Type 2']] || 0) + 1;
                }}
            }});
            
            const chartData = Object.entries(typeCount).map(([type, count]) => ({{
                type: type,
                count: count
            }}));
            
            const generationCountDiv = document.getElementById('generationCount');
            generationCountDiv.textContent = 'Pokémon in Generation ' + generation + ': ' + generationData.length;
            generationCountDiv.style.display = 'block';
            
            const typeColors = {{
                'Normal': 'grey',
                'Fighting': '#C03028',
                'Flying': '#A890F0',
                'Poison': '#A040A0',
                'Ground': '#8B4513',
                'Rock': '#B8A038',
                'Bug': '#A8B820',
                'Ghost': '#705898',
                'Steel': '#B8B8D0',
                'Fire': 'red',
                'Water': 'blue',
                'Grass': 'green',
                'Electric': 'yellow',
                'Psychic': '#F85888',
                'Ice': '#98D8D8',
                'Dragon': 'orange',
                'Dark': 'black',
                'Fairy': '#EE99AC',
                'Stellar': '#B8B8D0',
                'Unknown': '#999999'
            }};

            const spec = {{
                $schema: "https://vega.github.io/schema/vega-lite/v6.json",
                data: {{ values: chartData }},
                mark: {{ type: 'arc', tooltip: true }},
                encoding: {{
                    theta: {{
                        field: 'count',
                        type: 'quantitative'
                    }},
                    color: {{
                        field: 'type',
                        type: 'nominal',
                        scale: {{
                            domain: Object.keys(typeColors),
                            range: Object.values(typeColors)
                        }},
                        legend: {{
                            title: 'Type',
                            orient: 'right',
                            labelFontSize: 12,
                            titleFontSize: 14
                        }}
                    }},
                    tooltip: [
                        {{ field: 'type', type: 'nominal', title: 'Type' }},
                        {{ field: 'count', type: 'quantitative', title: 'Pokémon Count' }}
                    ]
                }},
                view: {{ stroke: null }},
                width: 500,
                height: 500
            }};
            
            document.getElementById('noPieSelection').style.display = 'none';
            vegaEmbed('#pieChart', spec);
        }}
        
        document.addEventListener('DOMContentLoaded', function() {{
            initializeGenerationDropdown();
        }});
    </script>
</body>
</html>
"""

html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pokémon Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/vega@5"></script>
    <script src="https://cdn.jsdelivr.net/npm/vega-lite@6"></script>
    <script src="https://cdn.jsdelivr.net/npm/vega-embed@6"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #3B4CCA 0%, #FF0000 100%);
            min-height: 100vh;
            padding: 0 20px 40px 20px;
            }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .search-section {{
            text-align: center;
            margin-bottom: 80px;
            margin-top: 40px;
        }}
        
        .search-title {{
            color: white;
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}
        
        .search-controls {{
            display: flex;
            gap: 10px;
            align-items: center;
            justify-content: center;
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
        }}
        
        .search-container {{
            position: relative;
            flex: 1;
        }}
        
        .randomize-button {{
            padding: 16px 24px;
            font-size: 18px;
            border: none;
            border-radius: 50px;
            background-color: white;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 600;
            white-space: nowrap;
        }}
        
        .randomize-button:hover {{
            box-shadow: 0 12px 40px rgba(0,0,0,0.3);
            transform: scale(1.05);
        }}
        
        .search-input {{
            width: 100%;
            padding: 16px 20px;
            font-size: 18px;
            border: none;
            border-radius: 50px;
            background-color: white;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
            font-weight: 500;
        }}
        
        .search-input:focus {{
            outline: none;
            box-shadow: 0 12px 40px rgba(0,0,0,0.3);
            transform: scale(1.02);
        }}
        
        .search-input::placeholder {{
            color: #999;
        }}
        
        .dropdown {{
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: white;
            border-radius: 0 0 20px 20px;
            margin-top: 5px;
            max-height: 400px;
            overflow-y: auto;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
            display: none;
            z-index: 1000;
        }}
        
        .dropdown.active {{
            display: block;
        }}
        
        .dropdown-item {{
            padding: 10px 20px;
            cursor: pointer;
            border-bottom: 1px solid #f0f0f0;
            transition: background-color 0.2s ease;
            text-align: left;
            font-weight: 500;
            color: #333;
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        
        .dropdown-item-icon {{
            width: 40px;
            height: 40px;
            flex-shrink: 0;
            object-fit: contain;
        }}
        
        .dropdown-item-text {{
            flex: 1;
        }}
        
        .dropdown-item:hover {{
            background-color: #f5f5f5;
            padding-left: 24px;
        }}
        
        .dropdown-item.selected {{
            background-color: #e8eaf6;
            color: #667eea;
        }}
        
        .stats-section {{
            background: #2a2a2a;
            padding: 60px 40px;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            margin-top: 100px;
            position: relative;
        }}
        
        .stats-title {{
            font-size: 28px;
            font-weight: bold;
            color: white;
            margin-bottom: 40px;
            text-align: center;
        }}
        
        .name-box {{
            position: absolute;
            top: 20px;
            left: 20px;
            background: #1a1a1a;
            color: white;
            padding: 20px 35px;
            border-radius: 12px;
            font-size: 36px;
            font-weight: bold;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }}
        
        .form-box {{
            position: absolute;
            top: 90px;
            left: 20px;
            background: #333;
            color: #ccc;
            padding: 8px 20px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 500;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            display: none;
        }}
        
        .form-box {{
            position: absolute;
            top: 90px;
            left: 20px;
            background: #333;
            color: #ccc;
            padding: 8px 20px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 500;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            display: none;
        }}
        
        .pokemon-info {{
            display: flex;
            gap: 15px;
            margin-bottom: 25px;
            margin-left: auto;
            margin-right: 40px;
            max-width: 400px;
            justify-content: center;
        }}
        
        .info-card {{
            color: white;
            padding: 15px 30px;
            border-radius: 10px;
            text-align: center;
            min-width: 120px;
            font-size: 20px;
            font-weight: bold;
        }}
        
        .stats-list {{
            color: white;
            font-size: 20px;
            line-height: 2;
            max-width: 400px;
            margin-left: auto;
            margin-right: 40px;
            padding: 20px;
        }}
        
        .stat-row {{
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #444;
        }}
        
        .stat-row:last-child {{
            border-bottom: none;
        }}
        
        .stat-row.total {{
            border-top: 2px solid #666;
            margin-top: 10px;
            padding-top: 15px;
            font-size: 22px;
        }}
        
        .bst-bar-container {{
            width: 100%;
            height: 30px;
            background: #1a1a1a;
            border-radius: 15px;
            margin-top: 15px;
            overflow: hidden;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);
        }}
        
        .bst-bar {{
            height: 100%;
            transition: width 0.5s ease, background 0.5s ease;
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            color: white;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }}
        
        .stat-name {{
            font-weight: 600;
        }}
        
        .stat-value {{
            font-weight: bold;
            color: #4ECDC4;
        }}
        
        .pokemon-sprite {{
            width: 300px;
            height: 300px;
            position: absolute;
            bottom: 20px;
            left: 20px;
            object-fit: contain;
        }}
        
        
        .no-selection {{
            text-align: center;
            color: #999;
            padding: 60px 20px;
            font-size: 18px;
        }}
    </style>
</head>
<body>

    <nav style="position: sticky; top: 0; background: white; padding: 15px 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); z-index: 1000; margin: 0; width: 100vw; margin-left: calc(-50vw + 50%);">

        <a href="./index.html" style="margin-left: 20px;" >PokéSearch</a>
        <a href="./generation.html" style="margin-left: 20px;" >Generation PokéTypes</a>
        <a href="./final.html#pokemon-comparison" style="margin-left: 20px;">PokéCompare</a>
        <a href="./final.html" style="margin-left: 20px;">Average PokéStats</a>
        <a href="./final.html#pokemon-scatter" style="margin-left: 20px;">PokéScatter</a>
        

    </nav>

    <div class="container">
            
            <div class="search-section">
                <div class="search-title">Pokémon Search Dashboard</div>
                <div class="search-controls">
                    <div class="search-container">
                        <input 
                            type="text" 
                            class="search-input" 
                            id="searchInput" 
                            placeholder="Search Pokémon (type a letter or name)..."
                            autocomplete="off"
                        >
                        <div class="dropdown" id="dropdown"></div>
                    </div>
                    <button class="randomize-button" id="randomizeButton">Randomize</button>
                </div>
            </div>
            
            
            <div class="stats-section" id="statsSection" style="display: none;">
                <div class="name-box" id="selectedName"></div>
                <div class="form-box" id="formBox"></div>
                
                <img id="pokemonSprite" class="pokemon-sprite" src="" alt="Pokémon sprite">
                
                <div class="pokemon-info" id="pokemonInfo"></div>
                
                <div class="stats-list" id="statsList"></div>
            </div>
            
            <div class="no-selection" id="noSelection">
                Select a Pokémon to view stats
            </div>
    </div>

    <script>
        const rawData = {data_json};
        let selectedPokemon = null;
        
        const typeColors = {{
            'Normal': '#A8A878',
            'Fighting': '#C03028',
            'Flying': '#A890F0',
            'Poison': '#A040A0',
            'Ground': '#E0C068',
            'Rock': '#B8A038',
            'Bug': '#A8B820',
            'Ghost': '#705898',
            'Steel': '#B8B8D0',
            'Fire': '#F08030',
            'Water': '#6890F0',
            'Grass': '#78C850',
            'Electric': '#F8D030',
            'Psychic': '#F85888',
            'Ice': '#98D8D8',
            'Dragon': '#7038F8',
            'Dark': '#705848',
            'Fairy': '#EE99AC',
            'Stellar': '#B8B8D0',
            'Unknown': '#68A090'
        }};
        
        const availableForms = {{}};
        rawData.forEach(pokemon => {{
            const num = String(pokemon.Number).padStart(4, '0');
            const sprite = pokemon.Sprite || '';
            if (sprite) {{
                
                const parts = sprite.split('_');
                if (parts.length >= 4) {{
                    const formId = parts[3];
                    if (!availableForms[num]) {{
                        availableForms[num] = new Set();
                    }}
                    availableForms[num].add(formId);
                }}
            }}
        }});
        
        
        Object.keys(availableForms).forEach(num => {{
            availableForms[num] = Array.from(availableForms[num]).sort();
        }});
        
        
        function getStatColumns() {{
            if (rawData.length === 0) return [];
            const firstRow = rawData[0];
            const excludeColumns = ['Number', 'Name', 'Form', 'Type 1', 'Type 2', 'Type1', 'Type2', 'Generation', 'Sprite'];
            
            return Object.keys(firstRow).filter(key => {{
                const val = firstRow[key];
                return typeof val === 'number' && !excludeColumns.includes(key);
            }});
        }}
        
        
        function getRandomFormId(pokemonNumber) {{
            const num = String(pokemonNumber).padStart(4, '0');
            const forms = availableForms[num];
            if (!forms || forms.length === 0) return null;
            return forms[Math.floor(Math.random() * forms.length)];
        }}
        
        
        function getRandomSprite(pokemonNumber) {{
            const num = String(pokemonNumber).padStart(4, '0');
            const formId = getRandomFormId(pokemonNumber);
            if (!formId) return null;
            
            
            const matching = rawData.find(p => {{
                const sprite = p.Sprite || '';
                const parts = sprite.split('_');
                return parts.length >= 4 && parts[2] === num && parts[3] === formId;
            }});
            
            return matching ? matching.Sprite : null;
        }}
        
        
        function updateDropdown() {{
            const searchValue = document.getElementById('searchInput').value.toLowerCase().trim();
            const dropdown = document.getElementById('dropdown');
            
            if (!searchValue) {{
                dropdown.classList.remove('active');
                return;
            }}
            
            const filtered = rawData.filter(pokemon => {{
                const name = pokemon.Name ? pokemon.Name.toLowerCase() : '';
                return name.includes(searchValue);
            }});
            
            dropdown.innerHTML = '';
            
            if (filtered.length === 0) {{
                dropdown.innerHTML = '<div class="dropdown-item" style="cursor: default; color: #999;">No results found</div>';
            }} else {{
                filtered.forEach(pokemon => {{
                    const item = document.createElement('div');
                    item.className = 'dropdown-item';
                    
                    
                    if (pokemon.Sprite && pokemon.Sprite !== null && pokemon.Sprite !== '') {{
                        const img = document.createElement('img');
                        img.className = 'dropdown-item-icon';
                        
                        const spritePath = 'Pok%C3%A9mon%20Icons/' + encodeURIComponent(pokemon.Sprite);
                        img.src = spritePath;
                        img.onerror = function() {{ this.style.display = 'none'; }};
                        item.appendChild(img);
                    }}
                    
                    
                    const textSpan = document.createElement('span');
                    textSpan.className = 'dropdown-item-text';
                    textSpan.textContent = pokemon.Name;
                    item.appendChild(textSpan);
                    
                    item.onclick = () => selectPokemon(pokemon);
                    dropdown.appendChild(item);
                }});
            }}
            
            dropdown.classList.add('active');
        }}
        
        
        function selectPokemon(pokemon) {{
            selectedPokemon = pokemon;
            document.getElementById('searchInput').value = pokemon.Name;
            document.getElementById('dropdown').classList.remove('active');
            displayStats();
        }}
        
        
        function displayStats() {{
            if (!selectedPokemon) return;
            
            const statsSection = document.getElementById('statsSection');
            const noSelection = document.getElementById('noSelection');
            
            statsSection.style.display = 'block';
            noSelection.style.display = 'none';
            
            
            document.getElementById('selectedName').textContent = selectedPokemon.Name;
            
            const formBox = document.getElementById('formBox');
            if (selectedPokemon.Form && selectedPokemon.Form !== '' && selectedPokemon.Form !== null) {{
                formBox.textContent = selectedPokemon.Form + ' Form';
                formBox.style.display = 'block';
            }} else {{
                formBox.style.display = 'none';
            }}
            
            const spriteImg = document.getElementById('pokemonSprite');
            const pokemonNumber = String(selectedPokemon.Number).padStart(4, '0');
            
            const indexImagePath = `index/${{pokemonNumber}}.png`;
            
            spriteImg.src = indexImagePath;
            spriteImg.style.display = 'block';
            
            let loadAttempts = 0;
            spriteImg.onerror = function() {{
                loadAttempts += 1;
                
                if (loadAttempts === 1) {{
                    let spriteUrl = selectedPokemon['Sprite'] || null;
                    
                    if (!spriteUrl) {{
                        const numForms = availableForms[pokemonNumber] || [];
                        if (numForms.length > 0) {{
                            spriteUrl = getRandomSprite(selectedPokemon.Number);
                        }}
                    }}
                    
                    if (spriteUrl) {{
                        const spritePathEncoded = 'Pok%C3%A9mon%20Icons/' + encodeURIComponent(spriteUrl);
                        this.src = spritePathEncoded;
                    }} else {{
                        this.style.display = 'none';
                    }}
                }} else if (loadAttempts === 2) {{
                    const spriteUrl = selectedPokemon['Sprite'];
                    if (spriteUrl) {{
                        const spritePathRawName = 'Pokémon Icons/' + spriteUrl;
                        this.src = spritePathRawName;
                    }} else {{
                        this.style.display = 'none';
                    }}
                }} else if (loadAttempts === 3) {{
                    const spriteUrl = selectedPokemon['Sprite'];
                    if (spriteUrl) {{
                        const spritePathEncodedRawFile = 'Pok%C3%A9mon%20Icons/' + spriteUrl;
                        this.src = spritePathEncodedRawFile;
                    }} else {{
                        this.style.display = 'none';
                    }}
                }} else {{
                    this.style.display = 'none';
                }}
            }};
            
            
            const statCols = getStatColumns();
            
            const type1 = selectedPokemon['Type 1'] || selectedPokemon['Type1'] || 'Unknown';
            const type2 = selectedPokemon['Type 2'] || selectedPokemon['Type2'];
            
            const type1Color = typeColors[type1] || '#999';
            const type2Color = type2 ? (typeColors[type2] || '#999') : null;
            
            let infoHtml = `
                <div class="info-card" style="background: ${{type1Color}};">
                    ${{type1}}
                </div>
            `;
            
            if (type2) {{
                infoHtml += `
                    <div class="info-card" style="background: ${{type2Color}};">
                        ${{type2}}
                    </div>
                `;
            }}
            
            document.getElementById('pokemonInfo').innerHTML = infoHtml;
            
            const statLabels = {{
                'HP': 'HP',
                'Attack': 'Attack',
                'Defense': 'Defense',
                'Sp. Atk': 'Special Attack',
                'Sp.Atk': 'Special Attack',
                'Sp.Attack': 'Special Attack',
                'SpA': 'Special Attack',
                'Sp. Def': 'Special Defense',
                'Sp.Def': 'Special Defense',
                'Sp.Defense': 'Special Defense',
                'SpD': 'Special Defense',
                'Speed': 'Speed'
            }};
            
            let statsHtml = '';
            let totalBST = 0;
            
            statCols.forEach(stat => {{
                const label = statLabels[stat] || stat;
                const value = selectedPokemon[stat];
                totalBST += value;
                statsHtml += `
                    <div class="stat-row">
                        <span class="stat-name">${{label}}:</span>
                        <span class="stat-value">${{value}}</span>
                    </div>
                `;
            }});
            
            const minBST = 180;
            const maxBST = 780;
            const normalizedBST = Math.max(0, Math.min(100, ((totalBST - minBST) / (maxBST - minBST)) * 100));
            
            const hue = (normalizedBST / 100) * 120;
            const saturation = 70;
            const lightness = 25 + (normalizedBST / 100) * 10;
            const bstColor = `hsl(${{hue}}, ${{saturation}}%, ${{lightness}}%)`;
            
            statsHtml += `
                <div class="stat-row total">
                    <span class="stat-name">Base Stat Total:</span>
                    <span class="stat-value">${{totalBST}}</span>
                </div>
                <div class="bst-bar-container">
                    <div class="bst-bar" style="width: ${{normalizedBST}}%; background: ${{bstColor}};">
                    </div>
                </div>
            `;
            
            document.getElementById('statsList').innerHTML = statsHtml;
        }}
        
        document.getElementById('searchInput').addEventListener('input', updateDropdown);
        document.getElementById('searchInput').addEventListener('keydown', function(e) {{
            if (e.key === 'Enter') {{
                const dropdown = document.getElementById('dropdown');
                const items = dropdown.querySelectorAll('.dropdown-item');
                if (items.length > 0) {{
                    items[0].click();
                }}
            }}
        }});
        
        document.getElementById('randomizeButton').addEventListener('click', function() {{
            if (rawData.length > 0) {{
                const randomIndex = Math.floor(Math.random() * rawData.length);
                selectPokemon(rawData[randomIndex]);
            }}
        }});
        
        document.addEventListener('click', function(e) {{
            if (!e.target.closest('.search-controls')) {{
                document.getElementById('dropdown').classList.remove('active');
            }}
        }});
        
        window.addEventListener('load', function() {{
            if (rawData.length > 0) {{
                const randomIndex = Math.floor(Math.random() * rawData.length);
                selectPokemon(rawData[randomIndex]);
            }}
        }});

    </script>
</body>
</html>
"""

# No longer generating HTML files - using the unified dashboard.html
print("Starting local server...")

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(Path(__file__).parent), **kwargs)
    
    def log_message(self, format, *args):
        pass


def start_server():
    server = HTTPServer(('localhost', 8000), Handler)
    server.serve_forever()

server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()


time.sleep(1)


url = "http://localhost:8000/dashboard.html"
print(f"Opening unified dashboard at {url}")
webbrowser.open(url)

print("Press Ctrl+C to stop the server")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n Server stopped")
