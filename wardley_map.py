import re


# your WardleyMap class here...
class WardleyMap():

	# Developed using https://regex101.com/
	_coords_regexs = "\[\s*([\d\.-]+)\s*,\s*([\d\.-]+)\s*\]"
	_node_regex = re.compile(r"^(\w+) (?:.*?//.*?)?([a-zA-Z0-9_.,/&' +)(?-]+?)\s+{COORDS}(\s+label\s+{COORDS})*".format(COORDS=_coords_regexs))
	_evolve_regex = re.compile(r"^evolve (?:.*?//.*?)?([\w \/',)(-]+?)\s+([\d\.-]+)(\s+label\s+{COORDS})*".format(COORDS=_coords_regexs))
	_pipeline_regex = re.compile(r"^pipeline ([a-zA-Z0-9_.,/&' )(?-]+?)(?:\s*//.*)?\s+\[\s*([\d\.]+)\s*,\s*([\d\.]+)\s*\]$")
	_note_regex = re.compile(r"^(\w+) (?:.*?//.*?)?([\S ]+?)\s+{COORDS}\s*".format(COORDS=_coords_regexs))

	def __init__(self, owm):
		# Defaults:
		self.title = None
		self.nodes = {}
		self.edges = []
		self.bluelines = []
		self.evolutions = {}
		self.evolves = {}
		self.pipelines = {}
		self.annotations = []
		self.annotation = {}
		self.notes = []
		self.style = None
		self.warnings = []

		# And load:
		for cl in owm.splitlines():
			cl = cl.strip()
			if not cl:
				continue

			elif cl.startswith('#'):
				# Skip comments...
				continue

			elif cl.startswith('//'):
				# Skip comments...
				continue

			elif cl.startswith('annotation '):
				warning_message = "Displaying annotation not supported yet"
				if warning_message not in self.warnings:
					self.warnings.append(warning_message)
				continue

			elif cl.startswith('annotations '):
				warning_message = "Displaying annotations not supported yet"
				if warning_message not in self.warnings:
					self.warnings.append(warning_message)
				continue

			elif cl.startswith('market '):
				warning_message = "Displaying market not supported yet"
				if warning_message not in self.warnings:
					self.warnings.append(warning_message)
				continue

			elif cl.startswith('pipeline '):
				match = self._pipeline_regex.search(cl)
				if match != None:
					matches = match.groups()
					pipeline = {
						'title': matches[0],
						'start_mat' : float(matches[1]),
						'end_mat' : float(matches[2]),
					}

					# And store it:
					self.pipelines[matches[0]] = pipeline
					continue
				else:
					self.warnings.append("Could not parse pipeline: %s" % cl)

			elif cl.startswith('evolution '):
				warning_message = "Displaying evolution not supported yet"
				if warning_message not in self.warnings:
					self.warnings.append(warning_message)
					continue

			if cl.startswith('title '):
				self.title = cl.split(' ', maxsplit=1)[1]
				continue

			elif cl.startswith('style '):
				self.style = cl.split(' ', maxsplit=1)[1]
				continue

			elif cl.startswith('anchor ') or cl.startswith('component '):
				# Use RegEx to split into fields:
				match = self._node_regex.search(cl)
				if match != None:
					matches = match.groups()
					node = {
						'type' : matches[0],
						'title': matches[1],
						'vis' : float(matches[2]),
						'mat' : float(matches[3])
					}
					# Handle label position adjustments:
					if matches[4]:
						node['label_x'] = float(matches[5])
						node['label_y'] = float(matches[6])
					else:
						# Default to a small additional offset:
						node['label_x'] = 2
						node['label_y'] = 2
					# And store it:
					self.nodes[node['title']] = node
				else:
					self.warnings.append("Could not parse component line: %s" % cl)

			elif cl.startswith('evolve '):
				match = self._evolve_regex.search(cl)
				if match != None:
					matches = match.groups()
					evolve = {
						'title': matches[0],
						'mat' : float(matches[1])
					}
					# Handle label position adjustments:
					if matches[3] is not None:
						evolve['label_x'] = float(matches[3])
					else:
						evolve['label_x'] = 2

					if matches[4] is not None:
						evolve['label_y'] = float(matches[4])
					else:
						evolve['label_y'] = 2

					# And store it:
					self.evolves[matches[0]] = evolve
					continue
				else:
					self.warnings.append("Could not parse evolve line: %s" % cl)

			elif "->" in cl:
				edge_parts = cl.split('->')
				if len(edge_parts) != 2:
					self.warnings.append(f"Unexpected format for edge definition: {cl}. Skipping this edge.")
					continue
				n_from, n_to = edge_parts
				self.edges.append([n_from.strip(), n_to.strip()])

			elif "+<>" in cl:
				edge_parts = cl.split('+<>')
				if len(edge_parts) != 2:
					self.warnings.append(f"Unexpected format for blueline definition: {cl}. Skipping this edge.")
					continue
				n_from, n_to = edge_parts
				self.bluelines.append([n_from.strip(), n_to.strip()])
				continue

			elif cl.startswith('note'):
				match = self._note_regex.search(cl)
				if match != None:
					matches = match.groups()
					note = {
						'text' : matches[1],
					}
					# Handle text position adjustments:
					if matches[2]:
						note['vis'] = float(matches[2])
						note['mat'] = float(matches[3])
					else:
						# Default to a small additional offset:
						note['vis'] = .2
						note['mat'] = .2
					# And store it:
					self.notes.append( note)
				else:
					self.warnings.append("Could not parse note line: %s" % cl)
			else:
				# Warn about lines we can't handle?
				self.warnings.append("Could not parse line: %s" % cl)

		self.warnings = list(set(self.warnings))


def wardley(map):

	# Parse the OWM syntax:
	wm = WardleyMap(map)

	if wm.style is None:
		wm.style = 'wardley'

	return wm

