/** @odoo-module */

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class StoreRequestDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.loadData();
    }

    async loadData() {
        const [storeRequestData, purchaseRequestData] = await Promise.all([
            // Load Store Request Status data
            this.orm.readGroup(
                'store.request',
                [['state', 'in', ['on siv', 'on request']]],
                ['state'],
                ['state']
            ),
            // Load Purchase Request Type data
            this.orm.readGroup(
                'purchase.request',
                [],
                ['purchase_type'],
                ['purchase_type']
            )
        ]);

        this.renderCharts(storeRequestData, purchaseRequestData);
    }

    renderCharts(storeRequestData, purchaseRequestData) {
        // Implement chart rendering using Chart.js
        this.renderStoreRequestChart(storeRequestData);
        this.renderPurchaseRequestChart(purchaseRequestData);
    }

    renderStoreRequestChart(data) {
        // Example using Chart.js
        const ctx = this.el.querySelector('#store_request_chart');
        if (!ctx) return;

        const labels = data.map(record => record.state);
        const values = data.map(record => record.__count);

        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: [
                        '#4CAF50',
                        '#2196F3'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Store Requests by Status'
                    }
                }
            }
        });
    }

    renderPurchaseRequestChart(data) {
        // Example using Chart.js
        const ctx = this.el.querySelector('#purchase_request_chart');
        if (!ctx) return;

        const labels = data.map(record => record.purchase_type);
        const values = data.map(record => record.__count);

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Purchase Requests',
                    data: values,
                    backgroundColor: '#2196F3'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Purchase Requests by Type'
                    }
                }
            }
        });
    }
}

StoreRequestDashboard.template = 'store_request.Dashboard';
StoreRequestDashboard.props = {};

registry.category("actions").add("store_request_dashboard", StoreRequestDashboard);
