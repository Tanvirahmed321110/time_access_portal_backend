/** @odoo-module **/

import { ListRenderer } from "@web/views/list/list_renderer";
import { patch } from "@web/core/utils/patch";
import { onMounted, onPatched } from "@odoo/owl";

patch(ListRenderer.prototype, {
    setup() {
        super.setup(...arguments);

        onMounted(() => {
            this._updateB2BPriceHeader();
        });

        onPatched(() => {
            this._updateB2BPriceHeader();
        });
    },

    _updateB2BPriceHeader() {
        if (this.props.list?.resModel !== "sale.order.line") {
            return;
        }

        const root = this.rootRef?.el;
        if (!root) {
            return;
        }

        const priceHeader = root.querySelector('thead th[data-name="price_unit"]');
        if (!priceHeader) {
            return;
        }

        const records = this.props.list.records || [];

        const hasB2BProduct = records.some((record) => {
            const value = record.data?.is_b2b_portal_line;
            return value === true || value === 1 || value === "true";
        });

        const label = hasB2BProduct ? "B2B Price" : "Unit Price";

        const labelEl =
            priceHeader.querySelector(".o_column_title") ||
            priceHeader.querySelector("span") ||
            priceHeader;

        labelEl.textContent = label;
    },
});