{% if coupons %}
    <ul>
        {% for coupon in coupons %}
            <li>{{ coupon.code }} - {{ coupon.discount }}% discount</li>
        {% endfor %}
    </ul>
{% else %}
    <p>No coupons available</p>
{% endif %}
