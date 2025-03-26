from flask import Flask, request, abort, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

# Replace with your actual Monday.com API key
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjQxMDM1MDMyNiwiYWFpIjoxMSwidWlkIjo1NTIyMDQ0LCJpYWQiOiIyMDI0LTA5LTEzVDExOjUyOjQzLjAwMFoiLCJwZXIiOiJtZTp3cml0ZSIsImFjdGlkIjozNzk1MywicmduIjoidXNlMSJ9.hwTlwMwtbhKdZsYcGT7UoENBLZUAxnfUXchj5RZJBz4"
API_URL = "https://api.monday.com/v2"

#------------------------------------------------
#------------------------------------------------
#------------------------------------------------
#------------------------------------------------
@app.route('/', methods=['GET'])
def home():
    print("Welcome")
    return "Welcome to the API!"

@app.route('/webhook', methods=['POST'])
def webhook():

        if request.method == 'POST':
            try:
                webhook_data = request.get_json()
                print("Received webhook data:",
                      webhook_data)  # Debugging: Print received data

                # Extract board ID and item ID from the webhook (adapt to your webhook's structure)
                board_id = webhook_data.get('event', {}).get('boardId', {})
                item_id = webhook_data.get('event', {}).get('pulseId', {})
                pulse_name = webhook_data.get('event', {}).get('pulseName', {})
                pulse_json = jsonify(pulse_name)
                print("Pulse:", pulse_name)

                if isinstance(pulse_name, str):
                    pulse_name = pulse_name.replace('"', '\\"')

                if not board_id:
                    print(
                        "Error: Could not extract board_id or item_id from webhook."
                    )
                    return jsonify(
                        {"error": "Missing board_id or item_id in webhook"}), 400

                # Information you want to send back to Monday.com (Column X)
                # Replace with the actual value

                # Construct the GraphQL mutation to update the column
                headers = {
                    "Authorization": API_KEY,
                    "Content-Type": "application/json"
                }

                query = f'mutation{{ change_simple_column_value (item_id: {item_id},board_id: {board_id}, column_id: "texto_1_mkn58839", value: "{pulse_name}") {{ id }} }}'
                data = {'query': query}

                response = requests.post(url=API_URL, json=data, headers=headers)

                if response.status_code == 200:
                    print("Successfully updated Monday.com column:",
                          response.json())
                    return jsonify({
                        "status": "success",
                        "message": "Column updated"
                    }), 200
                else:
                    print(
                        f"Error updating Monday.com column: {response.status_code} - {response.text}"
                    )
                    return jsonify({
                        "error": "Failed to update column",
                        "monday_response": response.text
                    }), response.status_code

            except (KeyError, TypeError, AttributeError) as e:
                print(f"Error processing webhook data: {e}")
                return jsonify({"error": "Error processing webhook data"}), 400
            except requests.exceptions.RequestException as e:
                print(f"Error communicating with Monday.com API: {e}")
                return jsonify(
                    {"error": "Error communicating with Monday.com API"}), 500
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                return jsonify({"error": "An unexpected error occurred"}), 500
        else:
            abort(400)


#------------------------------------------------
#------------------------------------------------
#------------------------------------------------
#------------------------------------------------


@app.route('/set_subitem_date', methods=['POST'])
def set_subitem_date():
    if request.method == 'POST':
        try:
            webhook_data = request.get_json()
            print("Received webhook data:",
                  webhook_data)  # Debugging: Print received data

            # Extract board ID and item ID from the webhook (adapt to your webhook's structure)
            item_id = webhook_data.get('event', {}).get('parentItemId', {})
            board_id = webhook_data.get('event',
                                        {}).get('parentItemBoardId', {})
            subitem_board_id = webhook_data.get('event', {}).get('boardId', {})
            subitem_id = webhook_data.get('event', {}).get('pulseId', {})
            subitem_number = webhook_data.get('event',
                                             {}).get('n_meros_mkm9dpdt', {})
            subitem_offset = webhook_data.get('event',
                                              {}).get('n_meros_mkmx3p62',
                                                      {}).get('value')
            subitem_json = jsonify(subitem_id)
            subitem_json = jsonify(subitem_number)
            n_meros_mkmx3p62_value = webhook_data.get('event', {}).get(
                'n_meros_mkmx3p62', {}).get('value', None)

            import time

            # ... (other code)

            time.sleep(2)  # Wait for 2 seconds (just for testing!)

            numbers_column = webhook_data.get('event',
                                              {}).get('n_meros_mkmx3p62')

            #if isinstance(pulse_name, str):
            #pulse_name = pulse_name.replace('"', '\\"')

            if not subitem_board_id:
                print(
                    "Error: Could not extract board_id or item_id from webhook."
                )
                return jsonify(
                    {"error": "Missing board_id or item_id in webhook"}), 400

            # Information you want to send back to Monday.com (Column X)
            # Replace with the actual value

            # Construct the GraphQL mutation to update the column
            headers = {
                "Authorization": API_KEY,
                "Content-Type": "application/json"
            }

            # First query to get the date
            date_query = f"""
            query {{items (ids: [{item_id}]) {{
                column_values {{
                    ... on DateValue {{
                        date
                    }}
                }}
            }}}}"""

            response = requests.post(url=API_URL,
                                     json={'query': date_query},
                                     headers=headers)
            date_data = response.json()

            # Extract the date value from response
            try:
                date_value = ""
                column_values = date_data['data']['items'][0]['column_values']
                for column in column_values:
                    if 'date' in column:
                        date_value = column['date']
                        break
            except (KeyError, IndexError):
                date_value = ""

            # Convert string date to datetime, add days, then format back to string
            current_date = datetime.strptime(date_value, '%Y-%m-%d')

            offset_days = int(list(subitem_offset)[0]) if subitem_offset else 0
            new_date = (current_date +
                        timedelta(days=offset_days)).strftime('%Y-%m-%d')

            # Second query to update with the extracted
            number_query = f"""
                query {{items (ids: [{subitem_id}]) {{
                    column_values {{
                        ... on NumbersValue {{
                            number
                              }}
                          }}
                      }}}}"""

            response = requests.post(url=API_URL,
                                     json={'query': number_query},
                                     headers=headers)
            number_data = response.json()

            try:
                number_value = ""
                column_values = number_data['data']['items'][0][
                    'column_values']
                for column in column_values:
                    if 'number' in column:
                        number_value = column['number']
                        break
            except (KeyError, IndexError):
                number_value = ""
                print("number value is:", number_value)

            # Convert string date to datetime, add days, then format back to string
            current_date = datetime.strptime(date_value, '%Y-%m-%d')

            offset_days = int(list(subitem_offset)[0]) if subitem_offset else 0
            new_date = (current_date +
                        timedelta(days=offset_days)).strftime('%Y-%m-%d')

            date_data = response.json()

            update_query = f'mutation{{ change_simple_column_value (item_id: {subitem_id}, board_id: {subitem_board_id}, column_id: "dup__of_data_mkmx6xcr", value: "{date_value}") {{ id }} }}'
            data = {'query': update_query}

            response = requests.post(url=API_URL, json=data, headers=headers)

            if number_value == 1:

                updateid_query = f'mutation{{ change_simple_column_value (item_id: {item_id}, board_id: {board_id}, column_id: "texto_1_mkncnqc9", value: "{subitem_id}") {{ id }} }}'
                data = {'query': updateid_query}

            response = requests.post(url=API_URL, json=data, headers=headers)

            if number_value == 1:

                updateboardid_query = f'mutation{{ change_simple_column_value (item_id: {item_id}, board_id: {board_id}, column_id: "texto_mknc26v7", value: "{subitem_board_id}") {{ id }} }}'
                data = {'query': updateboardid_query}

            response = requests.post(url=API_URL, json=data, headers=headers)

            if number_value == 2:

                updateid2_query = f'mutation{{ change_simple_column_value (item_id: {item_id}, board_id: {board_id}, column_id: "texto_2_mkncg9ba", value: "{subitem_id}") {{ id }} }}'
                data = {'query': updateid2_query}

            response = requests.post(url=API_URL, json=data, headers=headers)



            if response.status_code == 200:
                print("Successfully updated Monday.com column:",
                      response.json())
                return jsonify({
                    "status": "success",
                    "message": "Column updated"
                }), 200
            else:
                print(
                    f"Error updating Monday.com column: {response.status_code} - {response.text}"
                )
                return jsonify({
                    "error": "Failed to update column",
                    "monday_response": response.text
                }), response.status_code

        except (KeyError, TypeError, AttributeError) as e:
            print(f"Error processing webhook data: {e}")
            return jsonify({"error": "Error processing webhook data"}), 400
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Monday.com API: {e}")
            return jsonify(
                {"error": "Error communicating with Monday.com API"}), 500
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return jsonify({"error": "An unexpected error occurred"}), 500
    else:
        abort(400)


#------------------------------------------------
#------------------------------------------------
#------------------------------------------------
#------------------------------------------------


@app.route('/change_subitem_date', methods=['POST'])
def change_subitem_date():
    if request.method == 'POST':
        webhook_data = request.get_json()
        print("Received webhook data:", webhook_data)

        try:
            board_id = webhook_data.get('event', {}).get('boardId', {})
            item_id = webhook_data.get('event', {}).get('pulseId', {})
            pulse_name = webhook_data.get('event', {}).get('pulseName', {})
            print("Pulse:", pulse_name)

            if isinstance(pulse_name, str):
                pulse_name = pulse_name.replace('"', '\\"')

            if not board_id:
                print("Error: Could not extract board_id or item_id from webhook.")
                return jsonify({"error": "Missing board_id or item_id in webhook"}), 400

            headers = {"Authorization": API_KEY, "Content-Type": "application/json"}

            print("item é:", item_id)

            subitem1_query = f"""query {{ items (ids: ["{item_id}"]) {{ column_values (ids: ["texto_1_mkncnqc9"]) {{ ... on TextValue {{ text }} }} }} }}"""
            response = requests.post(url=API_URL, json={'query': subitem1_query}, headers=headers)
            subitem1 = response.json()
            subitem1_value = int(subitem1['data']['items'][0]['column_values'][0]['text'])
            
            print("Coluna subitem 1 é:", subitem1_value)
            

            subitem2_query = f"""query {{ items (ids: ["{item_id}"]) {{ column_values (ids: ["texto_2_mkncg9ba"]) {{ ... on TextValue {{ text }} }} }} }}"""
            response = requests.post(url=API_URL, json={'query': subitem2_query}, headers=headers)
            subitem2 = response.json()
            subitem2_value = int(subitem2['data']['items'][0]['column_values'][0]['text'])
            print("Coluna subitem 2 é:", subitem2_value)

            subitemboard_query = f"""query {{ items (ids: ["{item_id}"]) {{ column_values (ids: ["texto_mknc26v7"]) {{ ... on TextValue {{ text }} }} }} }}"""
            response = requests.post(url=API_URL, json={'query': subitemboard_query}, headers=headers)
            subitemboard = response.json()
            subitemboard_value = int(subitemboard['data']['items'][0]['column_values'][0]['text'])
            print("Subitem board é:", subitemboard_value)

            date_query = f"""query {{items (ids: [{item_id}]) {{ column_values {{ ... on DateValue {{ date }} }} }}}}"""
            response = requests.post(url=API_URL, json={'query': date_query}, headers=headers)
            date_data = response.json()

            
            try:
                date_value = ""
                column_values = date_data['data']['items'][0]['column_values']
                for column in column_values:
                    if 'date' in column:
                        date_value = column['date']
                        break
            except (KeyError, IndexError):
                date_value = ""
                print ("datevalue: " , date_value)
            

            current_date = datetime.strptime(date_value, '%Y-%m-%d')
            print ("currenttime:" , current_date)

            update_query = f"""
            mutation {{
              change_multiple_column_values (
                item_id: {subitem1_value},
                board_id: {subitemboard_value},
                column_values: "{{\\\"dup__of_data_mkmx6xcr\\\": \\\"{date_value}\\\", \\\"label_mkncg3sn\\\": \\\"Update date\\\"}}"
              ) {{
                id
              }}
            }}
            """
            data = {'query': update_query}
            response = requests.post(url=API_URL, json=data, headers=headers)


           
            update_query = f"""
            mutation {{
              change_multiple_column_values (
                item_id: {subitem2_value},
                board_id: {subitemboard_value},
                column_values: "{{\\\"dup__of_data_mkmx6xcr\\\": \\\"{date_value}\\\", \\\"label_mkncg3sn\\\": \\\"Update date\\\"}}"
              ) {{
                id
              }}
            }}
            """
            data = {'query': update_query}
            response = requests.post(url=API_URL, json=data, headers=headers)

            return jsonify({"success": True})

        except (KeyError, TypeError, AttributeError) as e:
            print(f"Error processing webhook data: {e}")
            return jsonify({"error": "Error processing webhook data"}), 400
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Monday.com API: {e}")
            return jsonify({"error": "Error communicating with Monday.com API"}), 500
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return jsonify({"error": "An unexpected error occurred"}), 500
    else:
        abort(400)

API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjI1OTU3MDMyMiwiYWFpIjoxMSwidWlkIjozNDE4MzA0NCwiaWFkIjoiMjAyMy0wNS0zMFQyMzo0NTo0MS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTMzMzU3NzgsInJnbiI6InVzZTEifQ.wo708JzzeAC1eqo1Gfq1yiPtB4tgppDhKqSPfjToRf8"
API_URL = "https://api.monday.com/v2"
BOARD_ID_TO_QUERY = 6712850239
COLUMN_ID_TO_GET = "conectar_quadros9__1"
COLUMN_ID_TO_UPDATE = "text_mkpdbm8b"

@app.route('/pressure-copy-items-to-txt', methods=['POST'])
def pressure_copy_items_to_txt():
    if request.method == 'POST':
        try:
            webhook_data = request.get_json()
            print("Received webhook data:", webhook_data)

            # Assuming the webhook payload has an event object containing the item ID
            item_id = webhook_data.get('event', {}).get('pulseId')

            if not item_id:
                print("Error: Could not extract item ID from webhook data.")
                return jsonify({"error": "Could not extract item ID from webhook data"}), 400

            print(f"Parsed Item ID from webhook: {item_id}")

            headers = {"Authorization": API_KEY, "Content-Type": "application/json"}

            # 1. Query Monday.com to get the value of conectar_quadros9__1
            query_get_value = f"""
                query {{
                  items (ids: [{item_id}], board_ids: [{BOARD_ID}]) {{
                    column_values (ids: ["{COLUMN_ID_TO_GET}"]) {{
                      text
                    }}
                  }}
                }}
            """
            data_get_value = {'query': query_get_value}
            monday_response_get = requests.post(url=API_URL, json=data_get_value, headers=headers)
            monday_data_get = monday_response_get.json()

            if monday_response_get.status_code == 200 and monday_data_get.get('data') and monday_data_get['data'].get('items') and monday_data_get['data']['items'][0].get('column_values'):
                value_to_paste = monday_data_get['data']['items'][0]['column_values'][0].get('text')
                print(f"Value of column '{COLUMN_ID_TO_GET}': {value_to_paste}")

                # 2. Update the column text_mkpdbm8b with the retrieved value
                if value_to_paste is not None:
                    mutation_update_value = f"""
                        mutation {{
                          change_simple_column_value (
                            item_id: {item_id},
                            board_id: {BOARD_ID},
                            column_id: "{COLUMN_ID_TO_UPDATE}",
                            value: "{value_to_paste.replace('"', '\\"')}"
                          ) {{
                            id
                          }}
                        }}
                    """
                    data_update_value = {'query': mutation_update_value}
                    monday_response_update = requests.post(url=API_URL, json=data_update_value, headers=headers)
                    monday_data_update = monday_response_update.json()

                    if monday_response_update.status_code == 200 and monday_data_update.get('data') and monday_data_update['data'].get('change_simple_column_value'):
                        print(f"Successfully updated column '{COLUMN_ID_TO_UPDATE}' with value: {value_to_paste}")
                        return jsonify({"message": f"Item ID: {item_id}, Column '{COLUMN_ID_TO_UPDATE}' updated with value from '{COLUMN_ID_TO_GET}'"}), 200
                    else:
                        print(f"Error updating column '{COLUMN_ID_TO_UPDATE}' on Monday.com: {monday_response_update.status_code} - {monday_response_update.text}")
                        return jsonify({"error": f"Error updating column '{COLUMN_ID_TO_UPDATE}' on Monday.com: {monday_response_update.status_code} - {monday_response_update.text}"}), monday_response_update.status_code
                else:
                    print(f"Value of column '{COLUMN_ID_TO_GET}' is None, skipping update.")
                    return jsonify({"message": f"Item ID: {item_id}, Column '{COLUMN_ID_TO_GET}' is None, skipping update of '{COLUMN_ID_TO_UPDATE}'"}), 200

            else:
                print(f"Error fetching value from column '{COLUMN_ID_TO_GET}' on Monday.com: {monday_response_get.status_code} - {monday_response_get.text}")
                return jsonify({"error": f"Error fetching value from column '{COLUMN_ID_TO_GET}' on Monday.com: {monday_response_get.status_code} - {monday_response_get.text}"}), monday_response_get.status_code

        except Exception as e:
            print(f"Error processing webhook data: {e}")
            return jsonify({"error": f"Error processing webhook data: {e}"}), 400
    else:
        return jsonify({"error": "Method not allowed"}), 405

     
