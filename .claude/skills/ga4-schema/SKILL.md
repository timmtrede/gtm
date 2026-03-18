# GA4 BigQuery Export Schema Reference

## Table Structure
GA4 exports to daily sharded tables: `analytics_287815421.events_YYYYMMDD`

## Top-Level Fields
| Field | Type | Description |
|---|---|---|
| `event_date` | STRING | Date (YYYYMMDD) |
| `event_timestamp` | INTEGER | Microseconds since epoch |
| `event_name` | STRING | Event name (e.g., `page_view`, `purchase`) |
| `event_params` | RECORD (REPEATED) | Key-value pairs for event parameters |
| `event_previous_timestamp` | INTEGER | Previous event timestamp |
| `event_value_in_usd` | FLOAT | Event value in USD |
| `user_id` | STRING | User-provided user ID |
| `user_pseudo_id` | STRING | Client ID (anonymous) |
| `user_properties` | RECORD (REPEATED) | User-scoped properties |
| `user_first_touch_timestamp` | INTEGER | First visit timestamp |
| `device` | RECORD | Device info (category, brand, model, os) |
| `geo` | RECORD | Geography (country, region, city) |
| `traffic_source` | RECORD | First-touch traffic source |
| `collected_traffic_source` | RECORD | Session-level traffic source |
| `session_traffic_source_last_click` | RECORD | Last-click attribution |
| `ecommerce` | RECORD | Ecommerce data (transaction_id, value, etc.) |
| `items` | RECORD (REPEATED) | Item-level ecommerce data |
| `stream_id` | STRING | Data stream ID |
| `platform` | STRING | Platform (WEB, IOS, ANDROID) |
| `is_active_user` | BOOLEAN | Active user flag |

## event_params Structure
Each element in `event_params` has:
- `key` (STRING) — parameter name
- `value.string_value` (STRING)
- `value.int_value` (INTEGER)
- `value.float_value` (FLOAT)
- `value.double_value` (FLOAT)

### Common event_params Keys
| Key | Type | Description |
|---|---|---|
| `page_location` | string | Full URL |
| `page_title` | string | Page title |
| `page_referrer` | string | Referrer URL |
| `ga_session_id` | int | Session ID |
| `ga_session_number` | int | Session count for user |
| `engagement_time_msec` | int | Engagement time (ms) |
| `source` | string | Traffic source |
| `medium` | string | Traffic medium |
| `campaign` | string | Campaign name |
| `entrances` | int | 1 if first event in session |

## items Structure (Ecommerce)
| Field | Type | Description |
|---|---|---|
| `item_id` | STRING | Product/SKU ID |
| `item_name` | STRING | Product name |
| `item_category` | STRING | Category |
| `item_list_name` | STRING | List context |
| `price` | FLOAT | Item price |
| `quantity` | INTEGER | Quantity |
| `index` | INTEGER | Position in list |

## ecommerce Structure
| Field | Type | Description |
|---|---|---|
| `transaction_id` | STRING | Transaction ID |
| `purchase_revenue` | FLOAT | Revenue |
| `tax` | FLOAT | Tax amount |
| `shipping` | FLOAT | Shipping cost |

## Unnesting Patterns

### Access event parameter
```sql
(SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'page_location') AS page_location
```

### Access item data
```sql
SELECT item.item_name, item.price
FROM `analytics_287815421.events_*`, UNNEST(items) AS item
WHERE event_name = 'purchase'
```

### Access user property
```sql
(SELECT value.string_value FROM UNNEST(user_properties) WHERE key = 'user_type') AS user_type
```

## Zipmend-Specific Parameters
Based on the Firestore event data, Zipmend sends these custom parameters:
| Key | Description |
|---|---|
| `page_type` | Page type (e.g., `booking_process`) |
| `content_group` | Content grouping |
| `user_type` | User type (e.g., `shipper`) |
| `order_origin` | Order origin (e.g., `online`) |
| `payment_type` | Payment method |
| `t_route` | Transport route (e.g., `DE_13629_Berlin-DE_14055_Berlin`) |
| `t_details` | Transport details |
| `t_date` | Transport date range |
