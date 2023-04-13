document.addEventListener("DOMContentLoaded", main);

function main(event) {
    document.getElementById("search-approach").addEventListener("click", function (event) {
        const base_url_elem = document.getElementById("base-url");
        const date_reference_elem = document.getElementById("date-reference");
        const n_approach_elem = document.getElementById("n-approach");

        if (base_url_elem !== null && date_reference_elem !== null && n_approach_elem !== null) {
            const base_url = base_url_elem.value;
            const date_reference = date_reference_elem.value;
            const n_approach = parseInt(+n_approach_elem.value);
            const regex_date = /^[0-9]{4}-[0-9]{2}-[0-9]{2}$/;
    
            if (base_url && regex_date.test(date_reference) === true && n_approach !== NaN) {
                let url = base_url + date_reference;
                if (n_approach > 0) {
                    url += `/${n_approach}`;
                }
                document.location.replace(url);
            }
        }
    });
}