<!-- offer_listing.tpl -->

{% if offers %}
<div class="offer-listing">
  <h4>Total Offers: {{ offers|length }}</h4>
  <ul>
    {% for offer in offers %}
    <li>{{ offer.title }} - {{ offer.price }}</li>
    {% endfor %}
  </ul>
</div>
{% else %}
<div class="offer-listing">
  <p>No offers available for this product.</p>
</div>
{% endif %}
