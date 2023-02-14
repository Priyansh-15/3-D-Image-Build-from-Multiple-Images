# Project Name : 3-D-Image-Build-from-Multiple-Images
# Made By - Priyansh Sharma

## ***You can find a detailed explanation of real life implementation of this project here in my Blog :*** https://priyansh15.medium.com/how-do-google-maps-actually-build-a-3d-environment-street-view-algorithm-explanation-1b64b7904c53

## Project Demo Implementation Video :

https://user-images.githubusercontent.com/77832407/185854755-a4f994ed-cc8b-46bb-9e56-f5c265054b3e.mp4


3D reconstruction from multiple images is the creation of three-dimensional models from a set of images.
***This Project Initially takes 3 Image Views as Input { Front View , Side View , Top View } and generates a 3D model corresponding to it .***

The process include :
## Contour detection : 
***A shape will have 2 contours created from the thickness of the figure, one of which envelopes it from the outer side and other from inside.***

<img src="https://user-images.githubusercontent.com/77832407/177065252-375ea4e4-4574-4ed2-bd59-fb48e1aea62f.png" width=250>         <img src="https://user-images.githubusercontent.com/77832407/177063529-306bf008-3342-4436-8fc0-a8ecc13a1bb8.png" height=350>

## Point location :
Given any point, it is necessary to determine with the point lies inside or outside a particular contour.

This function return
* +1 if point is outside contour,
* -1 if point is inside and
* 0 if point is on the contour

<img src="https://user-images.githubusercontent.com/77832407/177063596-aff74b06-486d-426f-a530-dfc5042c1c1d.png" width=350>

## Shape Detection of 2D image :

This step involves the recognition of 2D shapes that need to be converted into 3D solids using suitable algorithms.

***We will be using 6 shapes namely circle, triangle, square, rectangle, pentagon and hexagon as these are the basic building block of any 3D object.***

<img src="https://user-images.githubusercontent.com/77832407/177063619-6ff47c5c-1921-4b1d-b251-9f26fddf1418.png" width=350>         <img src="https://user-images.githubusercontent.com/77832407/177063626-4fd47ee7-b338-41d0-a346-498c8d0ec608.png" width=500>

So for example if given a solid 3D Cylinder and corresponding its Front , Side and top View Images .

![image](https://user-images.githubusercontent.com/77832407/177063752-0e640f54-ab8e-4626-971e-1ea14489c406.png)

The 'Dimensioning Function' will give the Information regarding each View Image like 'Shape' and 'Ratio'.

<img src="https://user-images.githubusercontent.com/77832407/177064043-8f265a5b-3bce-4304-89aa-223f65e56673.png" width=300>       <img src="https://user-images.githubusercontent.com/77832407/177064054-bbd1c922-2ded-44d6-a37b-375fe8b52aea.png" width=300>         <img src="https://user-images.githubusercontent.com/77832407/177064076-4e5a6d43-454e-4655-926e-b56f44a43a19.png" width=300>

Then 'Convert Function' is used to generate SCAD File and its Corresponding Point Cloud Representation .

<img src="https://user-images.githubusercontent.com/77832407/177064176-0d656a58-ad68-4103-8ec4-fe076af12275.png" width=350> 
<img src="https://user-images.githubusercontent.com/77832407/177064195-e18de834-5665-410d-940d-c2788fc38e06.png" width=350>

***If The given 3D model is a combination of Complex shapes then A binary tree is created for each parent-child. Here,
each shape node class object is a node in the binary tree, and each shape node is a child node of an empty node class
object. The empty node class only holds the string of scad syntax, including the operation between the two children.***

<img src="https://user-images.githubusercontent.com/77832407/177064593-70e539f0-7193-4aeb-b1eb-19b13489a274.png" width=450>

And depending on the properties of the shape detected we apply rotation and translation concept .

## Translation 

<img src="https://user-images.githubusercontent.com/77832407/177064749-f0ba33d9-4bfd-433c-8233-c7da7e59d102.png" width=350>        
<img src="https://user-images.githubusercontent.com/77832407/177064773-1f44fc07-1d30-4676-a864-a4cb06d83e43.png" width=350>

## Rotation 

<img src="https://user-images.githubusercontent.com/77832407/177064761-fe06f264-d4b8-4191-8cdb-fcc7422193a1.png" width=350>

Hence for Complex Shapes 

Input :

<img src="https://user-images.githubusercontent.com/77832407/177064862-2b9344d9-5046-4ba4-a22c-5c1586011e9d.png" width=350>

Output :

<img src="https://user-images.githubusercontent.com/77832407/177064891-d744686d-efd3-40b9-81ea-62dc8d2a306a.png" width=250>

## References and Credits :

***BOOK :***

***Automated 3D solid reconstruction from 2D CAD using OpenCV [Ajay B. Harisha, Abhishek R Prasadb]***

***GitHub :***

***Automated CAD model generator : https://github.com/bhajay/ACADGen***
