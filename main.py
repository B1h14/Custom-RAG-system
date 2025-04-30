import Request

if __name__ == "__main__":
    graph = Request.set_up(Request.API_KEY,Request.MODE)
    while(True):
        print("Enter your question:")
        user_input = input()
        if user_input == "exit":
            break
        print("Response :")
        print(Request.get_response(graph, user_input))



