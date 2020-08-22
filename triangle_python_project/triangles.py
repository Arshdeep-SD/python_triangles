from flask import Flask, render_template, request, jsonify
import json
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('triangles.html')

@app.route('/process', methods=['POST'])
def process():
	
	#print (request.is_json)
	req_data = request.get_json()
	points1 = req_data["points1"]
	points2 = req_data["points2"]
	print (points1)
	print (points2)
	
	in_points = []
	#in_points = [(4, 2), (1, 1), (3, 1), (4, 4), (1, 3), (4, 1)]
	
	in_points.insert(0,list(points1.pop().values()));
	in_points.insert(1,list(points1.pop().values()));
	in_points.insert(2,list(points1.pop().values()));
	
	in_points.insert(0,list(points2.pop().values()));
	in_points.insert(1,list(points2.pop().values()));
	in_points.insert(2,list(points2.pop().values()));
	
	print (in_points)
	
	t1 = points1
	t2 = points2

	#take inputs

	t1 = in_points[:3]
	t2 = in_points[3:6]
	
	s1 = sides(t1) 
	s2 = sides(t2)

	a1 = angles(s1)
	a2 = angles(s2)

	AB = [(t1[0], t1[1]), (t2[0], t2[1])]

	BC = [(t1[1], t1[2]), (t2[1], t2[2])]

	CA = [(t1[2], t1[0]), (t2[2], t2[0])]

	p = [[intersection(AB[0], AB[1]), AB[0], AB[1]],
		[intersection(AB[0], BC[1]), AB[0], BC[1]],
		[intersection(AB[0], CA[1]), AB[0], CA[1]],
		[intersection(BC[0], AB[1]), BC[0], AB[1]],
		[intersection(BC[0], BC[1]), BC[0], BC[1]],
		[intersection(BC[0], CA[1]), BC[0], CA[1]],
		[intersection(CA[0], AB[1]), CA[0], AB[1]],
		[intersection(CA[0], BC[1]), CA[0], BC[1]],
		[intersection(CA[0], CA[1]), CA[0], CA[1]]
	]
	
	intersection_points = [0]*9	

	for i in range(0, 9):
		
		if p[i][0] != 0: 
		
			intersection_points[i] = np.around(width(p[i][0], p[i][1][0]) + width(p[i][0], p[i][1][1]), decimals = 3)
			
		if intersection_points[i] != s1[i//3]:
		
			intersection_points[i] = 0

		#print(p[i][0])	
	final_pts = []
	j=0
	
	for i in range(0, 9):
		
		if intersection_points[i] != 0:
			
			intersection_points[i] = p[i][0]
			
			print(intersection_points[i])
			final_pts.insert(j,intersection_points[i])
			j = j+1
	
	intersection_points = json.dumps(final_pts)
	angles_val = []
	angles_val.insert(0,35)
	angles_val.insert(1,45.85555)
	angles_val.insert(2,18)
	angles_val_json = json.dumps(angles_val)
	
	return jsonify({"result": intersection_points,"intersection_angles":angles_val_json})

def det(a, b):
	
    return a[0] * b[1] - a[1] * b[0]
	
def width(a, b):
	
	return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5


def sides(t):

	lenghts = np.around([((t[0][0]-t[1][0])**2+(t[0][1]-t[1][1])**2)**0.5,
				((t[1][0]-t[2][0])**2+(t[1][1]-t[2][1])**2)**0.5,
				((t[2][0]-t[0][0])**2+(t[2][1]-t[0][1])**2)**0.5], decimals = 3)
				
	return lenghts

def angles(l):
	
	angles = np.around([np.rad2deg(np.arccos((l[0]**2+l[2]**2-l[1]**2)/(2*l[0]*l[2]))),
				np.rad2deg(np.arccos((l[1]**2+l[0]**2-l[2]**2)/(2*l[1]*l[0]))),
				np.rad2deg(np.arccos((l[2]**2+l[1]**2-l[0]**2)/(2*l[2]*l[1])))], decimals = 3)
	
	return angles

def intersection(line1, line2):

    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]) 

    div = det(xdiff, ydiff)
	
    if div == 0:
	
       return 0

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
	
    return x, y
if __name__ == '__main__':
	app.run(debug=True)