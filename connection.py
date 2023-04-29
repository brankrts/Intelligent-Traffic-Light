import socket 
import cv2 
import numpy as np


class Connection:
    
    def __init__(self,host="localhost",port=12345):
        self.port = port
        self.host = host
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.bind((self.host,self.port))
        
    def start_connection(self):
        self.socket.listen(5)
        conn,addr = self.socket.accept()
        return conn , addr

    def get_client_image(self,conn):
        dataFromClient = conn.recv(100000)
        image_array = np.frombuffer(dataFromClient, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        return image
    
    def close_connection(self):
        self.socket.close()      
            