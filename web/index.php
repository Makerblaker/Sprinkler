<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
	<link rel="stylesheet" href="css/bootstrap.min.css">
	<script src="js/jquery-3.3.1.min.js"></script>
	<script src="js/popper.min.js"></script>
	<script src="js/bootstrap.min.js"></script>
	<title>The Millers Sprinklers</title>
</head>

<body>
	<!-- Expanding nav bar -->
	<nav class="navbar navbar-expand-lg navbar-light bg-light">
		<a class="navbar-brand" href="#">
			<img src="img/sprinkler.jpg" width="30" height="30" class="d-inline-block align-top" alt="">
			The Miller Sprinklers
		</a>
		<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
		<span class="navbar-toggler-icon"></span>
		</button>
		<div class="collapse navbar-collapse" id="navbarNavDropdown">
			<ul class="navbar-nav">
				<li class="nav-item active">
					<a class="nav-link" href="#">Home  <span class="sr-only">(current)</span></a>
				</li>
				<li class="nav-item dropdown">
					<a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
						History
					</a>
					<div class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
						<a class="dropdown-item" href="#">One Week</a>
						<a class="dropdown-item" href="#">Two Weeks</a>
						<a class="dropdown-item" href="#">30 Days</a>
					</div>
				</li>
			</ul>
		</div>
	</nav>
	<!-- End of nav bar -->
	<?php
	if(isset($_GET["action"])) {
		if($_GET["action"] == "Start")
		{
			$sprinklerZone = $_POST["sprinklerZone"];
			$sprinklerDuration = $_POST["sprinklerDuration"];

			// Start python script here.
			exec("python /home/pi/Scripts/Sprinkler/water.py ".$sprinklerZone." ".$sprinklerDuration." 2>&1");
			?>
			<div class="alert alert-success" role="alert">
				<h4 class="alert-heading">Sprinker Started!</h4>
  				Zone <?php print $sprinklerZone; ?> for <?php print $sprinklerDuration; ?> minutes.
			</div>
			<?php
		}
	}
	?>
	<!-- Main Content -->
	<div class="container">
		<div class="row">
			<div class="col-sm">
				<form action="index.php?action=Start" method="POST">
					<div class="form-group">
						<label for="sprinklerZone">Zone</label>
						<input type="text" name="sprinklerZone" class="form-control" id="sprinklerZone" placeholder="Zone Number">
					</div>
					<div class="form-group">
						<label for="sprinklerDuration">Duration</label>
						<input type="text" name="sprinklerDuration" class="form-control" id="sprinklerDuration" aria-describedby="durationHelp" placeholder="Duration">
						<small id="durationHelp" class="form-text text-muted">Total run time in minutes.</small>
					</div>
					<button type="submit" class="btn btn-primary">Submit</button>
				</form>
			</div>
		</div>
	</div>
	<!-- End of Main Content -->
</body>

</html>