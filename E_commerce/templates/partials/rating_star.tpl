{% if rating %}
    <div class="rating">
        <span class="rating-value">{{ rating }}</span>
        <div class="stars">
            {% for i in "12345" %}
                {% if i <= rating %}
                    <i class="fas fa-star"></i>
                {% else %}
                    <i class="far fa-star"></i>
                {% endif %}
            {% endfor %}
        </div>
    </div>
{% else %}
    <p>No rating available</p>
{% endif %}
