import time
import board
import adafruit_dht
import psycopg2

sensor = adafruit_dht.DHT11(board.D4)

try:
    conn = psycopg2.connect(dbname='dht11', user='postgres', password='secret', host='host')
except:
    print('Can`t establish connection to database')

cursor = conn.cursor()

print("Старые данные:")
cursor.execute('SELECT * FROM history')
history = cursor.fetchall()
print(history, sep="\n")

print("Новые данные:")
while True:
    try:
        temperature_c = sensor.temperature
        humidity = sensor.humidity
        print(f"Date={time.time}, Temp={temperature_c}ºC, Humidity={humidity}%")
        cursor.execute(f"INSERT INTO history (date, temperature, humidity) VALUES (%s, %s, %s)", (time.time, temperature_c, humidity))

    except KeyboardInterrupt:
        break
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        sensor.exit()
        raise error
    
    
    time.sleep(3.0)

print("Остановка программы.")
cursor.close()
conn.close() 