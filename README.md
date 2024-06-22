# Setting Up Your Project

1. Set your Env Variables
2. Make virtual environmet :
   
   ```
   python -m venv myenv
   myenv\Scripts\activate
    ```

3. Install Flask and Dot-Env
   ```
    pip install flask
    pip install python-dotenv
   ```

4. Install OCR Dependencies
    ```
    pip install --upgrade azure-cognitiveservices-vision-computervision
    pip install pillow

    ```
5. Install Image Analysis Dependencies

    ```
    pip install azure-ai-vision-imageanalysis

    ```

6. Start the flask server
   
   ```
   python ./app.py

   ```

  
