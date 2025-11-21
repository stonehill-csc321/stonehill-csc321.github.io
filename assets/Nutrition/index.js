function autocompleteV4(){
    // Currently focused dropdown Item
    var currentFocus = -1;

    // List of all food data
    const food_data = data.map(n => n.food);

    // list of all searchBars in the application
    const searchBar = document.getElementById("searchBarV4");

    // Adding the input and key Events to each searchBar
    searchBar.addEventListener("input", _ => reloadDropDownList(searchBar));
    searchBar.addEventListener("keydown", e => dropDownKeyEvents(searchBar, e));

    // In the event a user clicks, all dropdowns will be removed except the drop-down passed as an argument
    document.addEventListener("click", e => closeAllLists(e.target));

    document.getElementById("food-selectV4").addEventListener("change", updateVis);

    // Handles the drop down key events
    function dropDownKeyEvents(input, e) {
        var x = document.getElementById(input.id + "autocomplete-list");
        if (!x) return;
        x = x.getElementsByTagName("div");

        if (e.keyCode === 40) { // UP
            currentFocus++;
            addActive(x);
        } else if (e.keyCode === 38) { // Down
            currentFocus--;
            addActive(x);
        } else if (e.keyCode === 9) { // Tab
            e.preventDefault();
            var values = document.getElementById(input.id + "autocomplete-list");

            if (!values) return;
            values = values.getElementsByTagName("input");

            if (!values) return;
            input.value = values[currentFocus > -1 ? currentFocus : 0].value;
            reloadDropDownList(input);
        } else if (e.keyCode === 13) { // Enter
            e.preventDefault();
            if (x) {
                x[currentFocus > -1 ? currentFocus : 0].click();
            }
        } else if (e.keyCode === 27) { // Escape
            closeAllLists();
        }
    }

    // Closes all drop-downs in the application and creates a new drop-down for the passed input
    function reloadDropDownList(input) {
        var val = input.value;
        currentFocus = -1;
        closeAllLists();

        if (!val) {
            return false;
        }

        var a = document.createElement("div");
        a.setAttribute("id", input.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        input.parentNode.appendChild(a);

        // Returns the count of the longest common sequence between two strings
        // Return Format: [start, end, count_longest_sequence]
        function CommonCharacters(s1, s2) {
            var maxCount = 0;
            var start = -1;

            for (var i = 0; i < s1.length - s2.length + 1; i++) {
                var count = 0;

                for (var j = i; j < s2.length + i; j++) {
                    if (s1[j].toUpperCase() !== s2[j - i].toUpperCase()) break;
                    count++;
                }

                if (count > maxCount) {
                    maxCount = count;
                    start = i;
                }

                if (count === s2.length) {
                    break;
                }
            }

            return [start, start + maxCount, maxCount];
        }

        // Creates a copy of the list of all foods
        // Sort the list by length (Shortest first)
        // Filters out any words that don't have at least 1 common character to the input value
        // Sorts the list in order of foods with the longest sequence of common character to the input value
        sorted_values = food_data.copyWithin()
            .sort((s1, s2) => s1.length - s2.length)
            .filter(s1 => CommonCharacters(s1, val)[2] > 0)
            .sort((s1, s2) => CommonCharacters(s2, val)[2] - CommonCharacters(s1, val)[2]);

        // Creates the html for each entry of the drop-down
        for (var i = 0; i < 15 && i < sorted_values.length; i++) {
            var b = document.createElement("div");
            var common = CommonCharacters(sorted_values[i], val);

            b.innerHTML = `${sorted_values[i].substring(0, common[0])}` +
                `<strong>${sorted_values[i].substring(common[0], common[1])}</strong>` +
                `${sorted_values[i].substring(common[1])}` +
                `<input type="hidden" value="${sorted_values[i]}">`;

            b.addEventListener("click", function(_) {
                closeAllLists();
                addEntryToTableV4(this.getElementsByTagName("input")[0].value);
                input.value = "";
            });

            a.appendChild(b);
        }
    }

    // Sets the classList for the currentFocus drop-down entry
    function addActive(x) {
        if (!x || x.length === 0) return false;
        removeActive(x);

        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        x[currentFocus].classList.add("autocomplete-active");
    }

    // Resets the classList for the all drop-down entries
    function removeActive(x) {
        for (var i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }

    // Removes all dropdowns except the drop-down passed as an argument
    function closeAllLists(element) {
        var x = document.getElementsByClassName("autocomplete-items");

        for (var i = 0; i < x.length; i++) {
            if (element !== x[i] && element != searchBar) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }

    // Adds passed food argument to the table. If the value already exists in the table, will be selected
    function addEntryToTableV4(food) {
        for(const row of document.getElementById("TableV4").getElementsByTagName("tr")) {
            if(row.firstChild.textContent === food) {
                row.classList.remove("selected-tableV4-row");
                row.classList.add("selected-tableV4-row");
                resetDoughnutChartSelection();
                return;
            }
        }

        var row = document.createElement("tr");
        var datum = data.find(e => e.food === food);
        var count_cell;

        for (const value of ["food", "count", "calories", "carbs", "protein", "fat", "sugar"]) {
            const table_data = document.createElement("td");

            table_data.attributeStyleMap.set("width", "500px");

            if (value === "count") {
                table_data.innerHTML += `<input value="1" maxlength="5">`;
                count_cell = table_data;
            } else {
                table_data.textContent = datum[value];
            }

            row.appendChild(table_data);
        }

        count_cell.firstChild.addEventListener("input", function(_) {
            var count = parseFloat(this.value);

            if(!count) return;
            if(count < 0) count = 1;

            for(const [i, value] of ["calories", "carbs", "protein", "fat", "sugar"].entries()) {
                row.children[i+2].textContent = Math.round(parseFloat(datum[value]) * count * 100) / 100;
            }

            updateVis();
        })

        row.addEventListener("click", function (e) {
            var tar = e.target;

            if (tar === count_cell.getElementsByTagName("input")[0]) {
                return;
            }

            if (this.classList.contains("selected-tableV4-row")) {
                this.classList.remove("selected-tableV4-row");
            } else {
                this.classList.add("selected-tableV4-row");
            }

            resetDoughnutChartSelection();
        });

        var table = document.getElementById("TableV4");
        table.insertBefore(row, table.children[1]);
        row.click();
    }

    // Resets the select options for the doughnut chart
    function resetDoughnutChartSelection() {
        const select = document.getElementById("food-selectV4");
        select.replaceChildren();

        for(const row of document.getElementById("TableV4").getElementsByClassName("selected-tableV4-row")) {
            const option = document.createElement("option");
            option.value = row.firstChild.textContent;
            option.textContent = row.firstChild.textContent;
            select.appendChild(option);
        }

        updateVis();
    }

    // Randomly selected entries to initially add to the table (Subject to change)
    addEntryToTableV4("bagel with ham egg cheese");
    addEntryToTableV4("profeel proteiinirahka valio");
    addEntryToTableV4("banana cream pie");
}