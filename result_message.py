def result_message(message, status_code, result):
    message = {
        "message": message,
        'status_code': status_code,
        'result': result
    }
    
    return message
