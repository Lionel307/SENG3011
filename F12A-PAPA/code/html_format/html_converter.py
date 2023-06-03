"""
A file to test other group's microservices
Written by Alex O'Neill (z5359415)
"""

def html_converter(result, location, hours):
  p0 = '<td class="p0">'
  p6 = '<td class="p6">'
  p7 = '<td class="p7">'
  p_red = '<td class="p0" style="color:red">'
  p_green = '<td class="p0" style="color:#00BB00">'
  p3 = '<td class="p3">'
  td = "</td>\n"
  def_html = """
<html>
<style>
table, th {
border: 1px solid black;
}
table tr {
border: 1px solid black;
}
table, th, td {
  border: 1px solid black;
}
table tr:last-child {
border: 0;
}
table.a {
table-layout: auto;
width: 850px;
}
.p0 {
font-family: "Times New Roman", Times, serif;
font-size: 25px;
text-align:center
}
.p1 {
font-family: "Times New Roman", Times, serif;
font-size: 25px;
}
.p2 {
font-family: "Times New Roman", Times, serif;
font-size: 25px;
font-weight:bold;
}
.p3 {
font-family: "Times New Roman", Times, serif;
font-size: 25px;
font-style: italic;
text-align:center
}
.p4 {
font-family: "Times New Roman", Times, serif;
font-size: 25px;
font-weight: bold;
font-style: italic;
}
.p5 {
font-family: "Times New Roman", Times, serif;
font-size: 60px;
font-weight: bold;
text-decoration: underline;
}
.p6 {
font-family: "Times New Roman", Times, serif;
font-size: 25px;
}
.p7 {
font-family: "Times New Roman", Times, serif;
font-size: 15px;
}
</style>
<center>
<p5 style="font-size:50px;font-weight: bold;text-decoration: underline;">Weather at """+location+"""</p5>
<br>
<p5 style="font-size:35px;font-weight: bold;text-decoration: underline;">For the past """+hours+""" hours</p5>
<table class="a">
    <tr class="p1">
        <th class="p1" style="width:20%">Date and Time</th>
        <th class="p1">Temperature (°C)</th>
        <th class="p1">Apparent Temperature (°C)</th>
        <th class="p1">Dew Point (°C)</th>
        <th class="p1">Relative Humidity (%)</th>
        <th class="p1">Wind (km/h)</th>
        <th class="p1">Rain (mm)</th>
    </tr>
  """

  
  # Average time

  for data in result:
    date = data["date"]
    time = data["time"]
    hour = time.split(":")[0]
    minute = time.split(":")[1]
    am_or_pm = "a.m."
    if int(time.split(":")[0]) >= 12:
        hour = str(int(hour)-12).zfill(2)
        am_or_pm = "p.m."
    if hour == "00":
        hour = "12"
    time_string = hour+":"+minute+" "+am_or_pm+"<br>"+date
    temperature = str(data["temperature"])
    apparent_temp = str(data["apparent_temp"])
    dew_point = str(data["dew_point"])
    relative_humidity = str(data["relative_humidity"])
    wind_direction = data["wind_direction"]
    wind_speed = str(data["wind_speed"])
    rain = str(data["rain"])
    wind = wind_speed + "<br>("+wind_direction+")"
    print(time_string)
    print(temperature)
    print(apparent_temp)
    print(dew_point)
    print(relative_humidity)
    print(wind)
    print(rain)
    def_html += "<tr>" + p0 + time_string + td + p0 + temperature + td + p0 + apparent_temp + td + p0 + dew_point + td + p0 + relative_humidity + td + p0 + wind + td + p0 + rain + td + "</tr>"
  def_html += """</tr>
      </table>"""
  print(def_html)
  return def_html
