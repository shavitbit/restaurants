# Restaurant API
This is a RESTful API for managing and searching restaurant data. The API provides functionality to initialize the database, search for restaurants based on various criteria, and specifically search by restaurant name.

## Features 
* Initialization: Ensure necessary database tables (restaurants, search_history) are created.
* Restaurant Search: Search for restaurants that are open at the time of the search with optional filters like name, style, vegetarian options, and delivery service.
* Name Search: Search for a restaurant by its name.

## Endpoints
### GET /search
Search for restaurants that are currently open. Optional query parameters allow for filtering by name, style, vegetarian options, and delivery service.
### query parameters
* restaurant_name (string, optional): The name of the restaurant.
* restaurant_style (string, optional): The style of cuisine (e.g., Italian, Chinese).
* vegetarian (boolean, optional): Whether the restaurant offers vegetarian options.
* deliveries (boolean, optional): Whether the restaurant offers delivery service.

```bash
GET /search?restaurant_name=Pizza&vegetarian=true&delivery=true
```

### GET /searchByRest
Search for a restaurant by its name.
### query parameters
* restaurant_name (string): The name of the restaurant.

```bash
GET /searchByRest?restaurant_name=Pizza
```

### POST /add_restaurant
Add one record to the restaurant table. Remove it in production! Its only for testing purposes.
Use the SSDT CI/CD to add unlimited records. 
### query parameters
* restaurant_name (string, require): The name of the restaurant.
* restaurant_style (string, require): The style of cuisine (e.g., Italian, Chinese).
* vegetarian (boolean, require): Whether the restaurant offers vegetarian options.
* deliveries (boolean, require): Whether the restaurant offers delivery service.
* timeOpen (string, require) The time that the restaurant open.
* timeClose (string, require) The time that the restaurant close .


```bash
curl -u admin:securepassword -X POST -H "Content-Type: application/json" -d '{"restaurantName": "Hummus Sababa"}' http://{app}/add_restaurant
```

### Future Enhancements
* RabbitMQ Integration: If time permits, integrating RabbitMQ to push data to the SQL database would be beneficial.
* SQL for Logs: Instead of traditional logs or blob tables, the API uses SQL to trace logs, allowing for easier data analysis by SQL experts. We can change it if require.
* Frontend Application: Adding a frontend to send requests to the API and placing the API within the SQL subnet for better integration and security.
* Error Handling - Currently, backend errors are being displayed.
