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
		<a class="navbar-brand" href="index.php">
			<img src="img/sprinkler.jpg" width="30" height="30" class="d-inline-block align-top" alt="">
			The Miller Sprinklers
		</a>
		<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
			<span class="navbar-toggler-icon"></span>
		</button>
		<div class="collapse navbar-collapse" id="navbarNavDropdown">
			<ul class="navbar-nav">
				<li class="nav-item active">
					<a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
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
	if (isset($_GET["action"])) {
		if ($_GET["action"] == "Start") {
			$sprinklerZone = $_POST["sprinklerZone"];
			$sprinklerDuration = $_POST["sprinklerDuration"];

			// Start python script here.
			exec("python3 /home/pi/Projects/Sprinkler/water.py " . $sprinklerZone . " " . $sprinklerDuration . " 2>&1");
			?>
			<div class="alert alert-success" role="alert">
				<h4 class="alert-heading">Sprinker Started!</h4>
				Zone <?php print $sprinklerZone; ?> for <?php print $sprinklerDuration; ?> minutes.
			</div>
		<?php
		}
	}
	if (isset($_GET["zone"])) {
		exec("python3 /home/pi/Projects/Sprinkler/zone.py " . $_GET["status"] . " " .$_GET["zone"] . " 2>&1");
		?>
			<div class="alert alert-warning" role="alert">
				Zone <?php print $_GET["zone"] . " " . $_GET["status"]; ?>
			</div>
		<?php
	}
?>
	<!-- Main Content -->
	<div class="container">
		<div class="row">
			<div class="col-sm">
				<form action="index.php?action=Start" method="POST">
					<div class="form-group">
						<label for="sprinklerZone">Zone</label>
						<?php
						$zones = array(0, 1, 2, 3);

						foreach ($zones as $zone) {
							?>
							<div class="form-check form-check-inline">
								<input class="form-check-input" type="radio" name="sprinklerZone" id="inlineRadio<?php echo $zone; ?>" value="<?php echo $zone; ?>">
								<label class="form-check-label" for="inlineRadio<?php echo $zone; ?>"><?php echo $zone; ?></label>
							</div>
						<?php
					}
					?>
					</div>
					<div class="form-group">
						<label for="sprinklerDuration">Duration</label>
						<input type="text" name="sprinklerDuration" class="form-control" id="sprinklerDuration" aria-describedby="durationHelp" placeholder="Duration">
						<small id="durationHelp" class="form-text text-muted">Total run time in minutes.</small>
					</div>
					<button type="submit" class="btn btn-primary">Submit</button>
					<br />
					<br />
					<table class="table">
						<tbody>
					<?php
					foreach ($zones as $zone) {
						echo "<tr>";
						echo "<td>Zone " . $zone . "</td>";
						echo "<td><a href=\"index.php?zone=" . $zone . "&status=ON\">ON</a>";
						echo "<td><a href=\"index.php?zone=" . $zone . "&status=OFF\">OFF</a>";
						echo "</tr>";
					}
					echo "</tbody>";
					echo "</table>";
					?>
				</form>
			</div>
		</div>
	</div>
	<!-- End of Main Content -->
</body>

</html>
