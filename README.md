# Dummy application

For playing around with api implementations.

## Endpoints

`GET /health`

**Response**

- `200 OK`

### list items

`GET /incense-sticks`

**Response**

- `200 OK`

```json
{
    "items" : "array of resources"
}
```

### new item

`POST /incense-sticks`

**Arguments**

- `"name":string` : "The name of the product"
- `"identifier":string` : "A unique identifier"
- `"manufacturer":string` : "The name of the company that made the product"
- `"number-of-sticks":integer` : "Number of sticks / box of product"

**Response**

- `201 CREATED`

```json
{
    "identifier" : "product-01",
    "name" : "Amber rose",
    "manufacturer" : "HEM",
    "number-of-sticks": 20
}
```

### item details

`GET /incense-stick/<identifier>`

**Response**

- `404 Not Found` if the product does not exist
- `200 OK` on success

```json
{
    "identifier" : "product-01",
    "name" : "Amber rose",
    "manufacturer" : "HEM",
    "number-of-sticks": 20
}
```

### item deletion

`DELETE /incense-stick/<identifier>`

**Response**

- `404 Not Found` if the product does not exist
- `204 No Content` on success

