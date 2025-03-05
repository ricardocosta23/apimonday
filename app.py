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
        data = request.get_json()
        challenge = data['challenge']

        return jsonify({'challenge': challenge})

        # print(request.json)
        # return 'success', 200
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
