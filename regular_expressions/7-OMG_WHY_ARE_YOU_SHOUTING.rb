#!/usr/bin/env ruby

regex = /[A-Z]/

ARGV.each do |arg|
  matches = arg.scan(regex)
  puts matches.join if matches.any?
end
