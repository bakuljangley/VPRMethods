InLoc: Indoor Visual Localization with Dense Matching and View Synthesis
------------------------------------------------------------------------

The original dataset description page can be found here: http://www.ok.sc.e.titech.ac.jp/INLOC/

For the conversion to kapture, we used the provided images as well as the camera poses. In detail, the kapture data consists of all cutout images from DUC1 and DUC2. For now, we do not provide the other buildings (DUC1 and DUC2 are used for the online benchmark).
The folder 'mapping' contains the training data (without images and scans) in kapture format, the folder 'query' contains the query data (without images) in kapture format.
In order to download the images, please follow these instructions: https://github.com/naver/kapture/blob/master/doc/datasets.adoc#inloc 

InLoc also provides 3D scans for each cutout image. These 3D files can be found in the same folder as the RGB images (if downloaded).
e.g.: 
image name: DUC_cutout_000_120_30.jpg
corresponding 3D file name: DUC_cutout_000_120_30.jpg.mat

Instructions to read the provided 3D data:
------------------------------------------

If you want to use the provided 3D data, please follow these steps (example code that needs to be modified accordingly).

1. Read the 3D file:

import scipy.io
depth = scipy.io.loadmat(path_to_mat_file)

Since the provided 3D data is not aligned with the world coordinate system, apply the provided transformations to do that. An aligned 3D point is then given in world coordinates and can be used to, e.g., compute the query images' pose in world coordinates.

2. Read the alignment data (this can certainly be done better): 

def read_alignments(path_to_alignment):
  aligns = {}
  with open(path_to_alignment, "r") as fid:
    while True:
      line = fid.readline()
      if not line:
        break
      if len(line) == 4:
        trans_nr = line[:-1]
        while line != 'After general icp:\n':
          line = fid.readline()
        line = fid.readline()
        p = []
        for i in range(4):
          elems = line.split(' ')
          line = fid.readline()
          for e in elems:
            if len(e) != 0:
              p.append(float(e))
        P = np.array(p).reshape(4,4)
        aligns[trans_nr] = P
  return aligns

aligns_DUC1 = read_alignments('mapping/DUC1_alignment/all_transformations.txt')
aligns_DUC2 = read_alignments('mapping/DUC2_alignment/all_transformations.txt')

Note: 
- The folders mapping/DUC1_alignment and mapping/DUC2_alignment come from the original dataset but are also destributed with InLoc in Kapture format.
- DUC1 contains one 360deg scan that is known to be wrong. See DUC1_alignment/know_incorrect.txt. 

3. Align one 3D point (example for building DUC1):

pt3d = depth['XYZcut'][int(y)][int(x)]
rgb = depth['RGBcut'][int(y)][int(x)]
pt3d_hom = np.ones(4,dtype=np.float32)
pt3d_hom[0:3] = pt3d.reshape(3)
pt3D_aligned = np.matmul(aligns_DUC1[trans_nr], pt3d_hom)

License:
--------

InLoc dataset is made available under the Open Database License: http://opendatacommons.org/licenses/odbl/1.0/. Any rights in individual contents of the database are licensed under the Database Contents License: http://opendatacommons.org/licenses/dbcl/1.0/
It contains information from Wustl Indoor RGBD dataset, which is made available here under the Open Database License http://opendatacommons.org/licenses/odbl/1.0/. 

See also:
---------
README.md ... original readme file
LICENSE.txt ... original license file