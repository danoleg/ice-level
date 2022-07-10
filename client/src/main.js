import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App.vue'
import IceThickness from './components/IceThickness.vue'
import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.min.css'
import 'vue-material/dist/theme/default.css'
import TreeView from "vue-json-tree-view"



Vue.use(VueRouter);
Vue.use(VueMaterial);
Vue.use(TreeView);

Vue.config.productionTip = false;

const routes = [
    {path: '/', component: IceThickness}
];

const router = new VueRouter({
    routes
});

new Vue({
    router,
    render: h => h(App),
    data() {
        return {
            iris_global_name: "",
            uploaded_json_file: ""
        };
    }
}).$mount('#app');
