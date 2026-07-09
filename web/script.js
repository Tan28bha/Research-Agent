let researchData = [];
let analysisData = {};
let accuracyData = {};


async function loadData() {

    try {

        const [
            researchResponse,
            analysisResponse,
            accuracyResponse
        ] = await Promise.all([

            fetch(
                "./data/final_results.json"
            ),

            fetch(
                "./data/analysis_summary.json"
            ),

            fetch(
                "./data/accuracy_summary.json"
            )

        ]);


        researchData =
            await researchResponse.json();


        analysisData =
            await analysisResponse.json();


        accuracyData =
            await accuracyResponse.json();


        initializePage();

    }

    catch (error) {

        console.error(
            "Failed to load research data:",
            error
        );

    }

}


function initializePage() {

    renderMetrics();

    renderOpportunityMap();

    populateCategoryFilter();

    renderTable();

    renderVerification();

    setupFilters();

}


function renderMetrics() {

    const metrics =
        analysisData.headline_metrics;


    document.getElementById(
        "total-apps"
    ).textContent =
        analysisData.total_apps;


    document.getElementById(
        "high-buildability"
    ).textContent =
        `${metrics.high_buildability_percentage}%`;


    document.getElementById(
        "self-serve"
    ).textContent =
        `${metrics.self_serve_percentage}%`;


    document.getElementById(
        "mcp-count"
    ).textContent =
        metrics.existing_mcp_count;

}


function createAppItem(app) {

    const item =
        document.createElement("div");


    item.className =
        "app-item";


    item.innerHTML = `

        <p class="app-name">

            ${escapeHTML(
        app.app_name
    )}

        </p>

        <p class="app-blocker">

            ${formatLabel(
        app.primary_blocker
    )}

        </p>

    `;


    return item;

}


function renderOpportunityMap() {

    const buildNow =
        researchData
            .filter(
                app =>
                    app.buildability
                    === "high"
            )
            .slice(0, 8);


    const investigate =
        researchData
            .filter(
                app =>
                    app.buildability
                    === "medium"
            )
            .slice(0, 8);


    const outreach =
        researchData
            .filter(
                app =>
                    app.buildability
                    === "low"
            )
            .slice(0, 8);


    renderAppList(
        "build-now-list",
        buildNow
    );


    renderAppList(
        "investigate-list",
        investigate
    );


    renderAppList(
        "outreach-list",
        outreach
    );

}


function renderAppList(
    elementId,
    apps
) {

    const container =
        document.getElementById(
            elementId
        );


    container.innerHTML = "";


    apps.forEach(app => {

        container.appendChild(
            createAppItem(app)
        );

    });

}


function populateCategoryFilter() {

    const filter =
        document.getElementById(
            "category-filter"
        );


    const categories = [

        ...new Set(

            researchData.map(
                app => app.category
            )

        )

    ].sort();


    categories.forEach(category => {

        const option =
            document.createElement(
                "option"
            );


        option.value =
            category;


        option.textContent =
            category;


        filter.appendChild(
            option
        );

    });

}


function renderTable(
    data = researchData
) {

    const tableBody =
        document.getElementById(
            "research-table-body"
        );


    tableBody.innerHTML = "";


    data.forEach(app => {

        const row =
            document.createElement(
                "tr"
            );


        const evidence =
            app.evidence
                && app.evidence.length > 0

                ? app.evidence[0].url

                : null;


        const authMethods =
            Array.isArray(
                app.auth_methods
            )

                ? app.auth_methods.join(
                    ", "
                )

                : "Unknown";


        const confidence =
            Math.round(

                (
                    app.confidence_score
                    || 0
                )

                * 100

            );


        row.innerHTML = `

            <td>

                ${escapeHTML(
            app.app_name
        )}

            </td>


            <td>

                ${escapeHTML(
            app.category
        )}

            </td>


            <td>

                ${escapeHTML(
            authMethods
        )}

            </td>


            <td>

                ${formatLabel(
            app.access_model
        )}

            </td>


            <td>

                ${formatLabel(
            app.api_breadth
        )}

            </td>


            <td>

                ${app.existing_mcp
                ? "Yes"
                : "No"
            }

            </td>


            <td>

                <span class="
                    status
                    status-${app.buildability}
                ">

                    ${escapeHTML(
                app.buildability
            ).toUpperCase()}

                </span>

            </td>


            <td>

                ${confidence}%

            </td>


            <td>

                ${evidence

                ? `

                            <a

                                class="evidence-link"

                                href="${escapeAttribute(
                    evidence
                )}"

                                target="_blank"

                                rel="noopener noreferrer"

                            >

                                View ↗

                            </a>

                        `

                : "—"
            }

            </td>

        `;


        tableBody.appendChild(
            row
        );

    });


    document.getElementById(
        "table-count"
    ).textContent =

        `Showing ${data.length} of ${researchData.length} applications`;

}


function setupFilters() {

    const searchInput =
        document.getElementById(
            "search-input"
        );


    const categoryFilter =
        document.getElementById(
            "category-filter"
        );


    const buildabilityFilter =
        document.getElementById(
            "buildability-filter"
        );


    function applyFilters() {

        const search =
            searchInput.value
                .toLowerCase()
                .trim();


        const category =
            categoryFilter.value;


        const buildability =
            buildabilityFilter.value;


        const filtered =
            researchData.filter(app => {

                const matchesSearch =

                    app.app_name
                        .toLowerCase()
                        .includes(search);


                const matchesCategory =

                    category === "all"

                    ||

                    app.category === category;


                const matchesBuildability =

                    buildability === "all"

                    ||

                    app.buildability
                    === buildability;


                return (

                    matchesSearch

                    &&

                    matchesCategory

                    &&

                    matchesBuildability

                );

            });


        renderTable(
            filtered
        );

    }


    searchInput.addEventListener(
        "input",
        applyFilters
    );


    categoryFilter.addEventListener(
        "change",
        applyFilters
    );


    buildabilityFilter.addEventListener(
        "change",
        applyFilters
    );

}


function renderVerification() {

    const firstConfidence =

        (
            accuracyData
                .first_pass_average_confidence

            || 0
        )

        * 100;


    const finalConfidence =

        (
            accuracyData
                .final_average_confidence

            || 0
        )

        * 100;


    document.getElementById(
        "first-confidence"
    ).textContent =

        `${firstConfidence.toFixed(1)}%`;


    document.getElementById(
        "final-confidence"
    ).textContent =

        `${finalConfidence.toFixed(1)}%`;

}


function formatLabel(value) {

    if (!value) {

        return "Unknown";

    }


    return value

        .replaceAll(
            "_",
            " "
        )

        .replace(
            /\b\w/g,

            character =>
                character.toUpperCase()
        );

}


function escapeHTML(value) {

    const element =
        document.createElement(
            "div"
        );


    element.textContent =
        value || "";


    return element.innerHTML;

}


function escapeAttribute(value) {

    return String(value)

        .replaceAll(
            "&",
            "&amp;"
        )

        .replaceAll(
            "\"",
            "&quot;"
        )

        .replaceAll(
            "<",
            "&lt;"
        )

        .replaceAll(
            ">",
            "&gt;"
        );

}


loadData();