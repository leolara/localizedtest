Vue.config.devtools = false;
Vue.config.productionTip = false;
console.clear();
new Vue({
    el: "#app",

    /* Initial state */
    data() {
        return {
            searchName: "",
            searchProfessor: "",
            searchTime: "",
            timesOptions: ['08:00', '09:00', '10:00', '11:00', '13:00', '14:00', '15:00', '16:00'],
            totalItems: 0,
            items: [],
            loading: true,
            pagination: {},
            headers: [
                { text: "Name", value: "name" },
                { text: "Professor", value: "professor" },
                { text: "Cost", value: "cost" },
                { text: "Times", value: "times" }
            ]
        };
    },

    /* Refresh from API on state change */
    watch: {
        params: {
            handler() {
                this.getDataFromApi().then(data => {
                    console.log("GETDATA");
                    this.items = data.items;
                    this.totalItems = data.total;
                });
            },
            deep: true
        }
    },

    /* Initial data load */
    mounted() {
        this.getDataFromApi().then(data => {
            this.items = data.items;
            this.totalItems = data.total;
        });
    },

    /* Defines state changes that produce refresh from API */
    computed: {
        params(nv) {
            return {
                ...this.pagination,
                searchName: this.searchName,
                searchProfessor: this.searchProfessor,
                searchTime: this.searchTime
            };
        }
    },

    methods: {
        /* Calculates serverurl to do GET to based on the Vue state */
        getServerUrl() {
            let serverurl =
                "http://127.0.0.1:8000/api/courses?page=" +
                this.pagination.page;

            console.log()
            if (this.searchName) {
                serverurl += "&name=" + this.searchName;
            }

            if (this.searchProfessor) {
                serverurl += "&professor=" + this.searchProfessor;
            }

            if (this.searchTime) {
                serverurl += "&times_hour=" + encodeURIComponent(this.searchTime);
            }

            if (
                this.pagination.rowsPerPage &&
                this.pagination.rowsPerPage != -1
            ) {
                serverurl += "&page_size=" + this.pagination.rowsPerPage;
            }

            if (this.pagination.sortBy) {
                serverurl += "&sortBy=" + this.pagination.sortBy;
                if (this.pagination.descending) {
                    serverurl += "&dir=desc";
                } else {
                    serverurl += "&dir=asc";
                }
            }

            return serverurl;
        },
        /* Transformations for the presentation layer of the data coming from the API */
        processDataFromAPI(data) {
            data.results = data.results.map(item => {
                item.times = item.times.join();
                return item;
            });

            return {
                items: data.results,
                total: data.count
            };
        },
        /* Fetches new data from the API */
        doFetch(serverurl) {
            this.loading = true;
            return fetch(serverurl)
                .then(result => result.json())
                .then(this.processDataFromAPI)
                .then((data) =>{
                    this.loading = false;
                    return data;
                })
                .catch(function (e) {
                    console.log(e);
                });
        },
        /* Refreshes state based on response from API,
        it is called automatically by Vue on change of state */
        getDataFromApi() {
            const serverurl = this.getServerUrl();

            return this.doFetch(serverurl);
        }
    }
});
