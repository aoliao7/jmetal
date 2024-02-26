import numpy as np

from jmetal.problem.multiobjective.mapping import mapping

# from mapping import mapping


# 把 B737-900 简称为 B739，A带头同理,B787-9改为B789,EMB190改为E190
def get_model2():

    total_model = set()
    model = [tuple() for _ in range(60)]

    s1 = {"A321", "B734", "B738", "B739", "B737-MAX8", "B737-MAX9", "B737-MAX10", "ARJ21"}
    s2 = {"A319", "A320", "B733", "B735", "B736", "B737", "B737-MAX7", "E190", "C919"}
    model[mapping(1)] = tuple([s1, s2])
    model[mapping(305)] = tuple([s1, s2])
    model[mapping(306)] = tuple([s1, s2])
    total_model = total_model | s1 | s2

    s1 = {"A321", "B734", "B738", "B739", "B737-MAX8", "B737-MAX9", "B737-MAX10"}
    s2 = {"A319", "A320", "B733", "B735", "B736", "B737", "B737-MAX7", "EMB190", "C919"}
    model[mapping(2)] = tuple([s1, s2])
    model[mapping(5)] = tuple([s1, s2])
    model[mapping(6)] = tuple([s1, s2])
    model[mapping(313)] = tuple([s1, s2])
    model[mapping(314)] = tuple([s1, s2])
    model[mapping(315)] = tuple([s1, s2])
    model[mapping(317)] = tuple([s1, s2])
    model[mapping(318)] = tuple([s1, s2])
    model[mapping(320)] = tuple([s1, s2])
    model[mapping(321)] = tuple([s1, s2])
    total_model = total_model | s1 | s2

    s1 = {"A321", "B734", "B738", "B739", "B737-MAX8", "B737-MAX9", "ARJ21"}
    s2 = {"B732", "B733", "B735", "B736", "B737", "B737-MAX7", "A318", "A319", "A320", "E190", "C919"}
    model[mapping(4)] = tuple([s1, s2])
    model[mapping(7)] = tuple([s1, s2])
    total_model = total_model | s1 | s2

    s1 = {"A321", "B734", "B738", "B739", "B737-MAX8", "B737-MAX9", "B737-MAX10", "ARJ21"}
    s2 = {"B732", "B733", "B735", "B736", "B737", "B737-MAX7", "A319", "A320", "E190", "C919"}
    model[mapping(10)] = tuple([s1, s2])
    model[mapping(11)] = tuple([s1, s2])
    model[mapping(12)] = tuple([s1, s2])
    model[mapping(13)] = tuple([s1, s2])
    model[mapping(15)] = tuple([s1, s2])
    model[mapping(16)] = tuple([s1, s2])
    total_model = total_model | s1 | s2

    s1 = {"A321", "B734", "B738", "B739", "B737-MAX8", "B737-MAX9", "B737-MAX10", "ARJ21"}
    s2 = {"B732", "B733", "B735", "B736", "B737", "B737-MAX7", "A319", "A320", "E190"}
    model[mapping(14)] = tuple([s1, s2])
    total_model = total_model | s1 | s2

    s1 = {"B738", "B739", "B737-MAX8", "B737-MAX9", "B737-MAX10", "A321", "ARJ21"}
    s2 = {"B732", "B733", "B734", "B735", "B736", "B737", "B737-MAX7", "A319", "A320", "E190", "C919"}
    model[mapping(21)] = tuple([s1, s2])
    model[mapping(22)] = tuple([s1, s2])
    model[mapping(23)] = tuple([s1, s2])
    model[mapping(24)] = tuple([s1, s2])
    model[mapping(25)] = tuple([s1, s2])
    model[mapping(26)] = tuple([s1, s2])
    total_model = total_model | s1 | s2

    s1 = {"A321", "B734", "B738", "B739", "B737-MAX8", "B737-MAX9", "B737-MAX10", "ARJ21"}
    s2 = {"A319", "A320", "B733", "B735", "B736", "B737", "B737-MAX7", "C919"}
    model[mapping(307)] = tuple([s1, s2])
    total_model = total_model | s1 | s2

    s1 = {"A321", "B734", "B738", "B739", "B737-MAX8", "B737-MAX9", "B737-MAX10"}
    s2 = {"A319", "A320", "B733", "B735", "B736", "B737", "B737-MAX7", "C919"}
    model[mapping(316)] = tuple([s1, s2])
    total_model = total_model | s1 | s2

    s1 = {"B753", "B763", "B767-300ER"}
    s2 = {"B734", "B738", "B739", "B737-MAX8", "B737-MAX9", "B737-MAX10", "A321", "B752", "B762", "A300", "ARJ21"}
    s3 = {"B733", "B736", "B737", "B737-MAX7", "A319", "A320", "E190", "C919"}
    model[mapping(308)] = tuple([s1, s2, s3])
    model[mapping(312)] = tuple([s1, s2, s3])
    total_model = total_model | s1 | s2

    s1 = {"A346", "B773", "B777-300ER", "A350-1000"}
    s2 = {"B763", "B767-300ER", "B753", "A345", "B744", "B789", "A359"}
    s3 = {"B772", "A342", "A333"}
    s4 = {"B752", "B762", "B734", "B738", "B739", "B737-MAX8", "B737-MAX9", "B737-MAX10", "A312", "A300", "B747SP"}
    s5 = {"B733", "B736", "B737", "A319", "A320", "A310", "E190", "C919"}
    model[mapping(309)] = tuple([s1, s2, s3, s4, s5])
    total_model = total_model | s1 | s2 | s3 | s4 | s5

    s1 = {"A346", "B773", "B777-300ER", "A350-1000"}
    s2 = {"B744", "A359"}
    s3 = {"B763", "B767-300ER", "B753", "A345"}
    s4 = {"B772", "A342", "A333", "A332"}
    s5 = {"B752", "B762", "B734", "B738", "B739", "B737-MAX8", "B737-MAX9", "B737-MAX10", "A321", "A300", "B747SP"}
    s6 = {"B733", "B736", "B737", "B737-MAX7", "A319", "A320", "A310", "E190", "C919"}
    model[mapping(310)] = tuple([s1, s2, s3, s4, s5, s6])
    total_model = total_model | s1 | s2 | s3 | s4 | s5 | s6

    s1 = {"A346", "B773", "B777-300ER", "A350-1000"}
    s2 = {"B789", "A359"}
    s3 = {"B763", "B767-300ER", "B753", "A343", "A345", "B744", "B788"}
    s4 = {"B772", "A342", "A333", "A332"}
    s5 = {"B752", "B762", "B734", "B738", "B739", "B737-MAX8", "B737-MAX9", "B737-MAX10", "A321", "A300", "B747SP"}
    s6 = {"B733", "B736", "B737", "B737-MAX7", "A319", "A320", "A310", "E190", "C919"}
    model[mapping(311)] = tuple([s1, s2, s3, s4, s5, s6])
    total_model = total_model | s1 | s2 | s3 | s4 | s5 | s6

    s1 = {"A346", "B773", "B777-300ER", "A350-1000"}
    s2 = {"B789", "A359"}
    s3 = {"B763", "B767-300ER", "B753", "A343", "A345", "B744"}
    s4 = {"B772", "A342", "A333", "A332"}
    s5 = {"B752", "B762", "B734", "B738", "B739", "B737-MAX8", "B737-MAX9", "B737-MAX10", "A321", "A300", "B747SP"}
    s6 = {"B733", "B736", "B737", "B737-MAX7", "A319", "A320", "A310", "E190", "C919"}
    model[mapping(319)] = tuple([s1, s2, s3, s4, s5, s6])
    total_model = total_model | s1 | s2 | s3 | s4 | s5 | s6

    s1 = {"B738", "B739", "B737-MAX8", "B737-MAX9", "B737-MAX10", "A321", "ARJ21"}
    s2 = {"B733", "B734", "B735", "B736", "B737", "B737-MAX7", "A320", "A319", "E190", "C919"}
    model[mapping(326)] = tuple([s1, s2])
    model[mapping(327)] = tuple([s1, s2])
    model[mapping(328)] = tuple([s1, s2])
    model[mapping(329)] = tuple([s1, s2])
    model[mapping(330)] = tuple([s1, s2])
    model[mapping(331)] = tuple([s1, s2])
    model[mapping(332)] = tuple([s1, s2])
    model[mapping(516)] = tuple([s1, s2])
    model[mapping(517)] = tuple([s1, s2])
    model[mapping(518)] = tuple([s1, s2])
    model[mapping(519)] = tuple([s1, s2])
    total_model = total_model | s1 | s2

    s1 = {"A346", "B773", "B777-300ER"}
    s2 = {"B744", "A345", "B789", "A359"}
    s3 = {"A333", "A342", "B772", "B763", "B767-300ER", "B753", "B757-300ER", "B788"}
    s4 = {"A321", "B738", "B739", "B737-MAX8", "B737-MAX9", "B737-MAX10", "B752", "B762", "A300", "A332", "ARJ21"}
    s5 = {"B733", "B734", "B736", "B737", "B737-MAX7", "A320", "B747SP", "E190", "C919"}
    model[mapping(510)] = tuple([s1, s2, s3, s4, s5])
    model[mapping(511)] = tuple([s1, s2, s3, s4, s5])
    model[mapping(512)] = tuple([s1, s2, s3, s4, s5])
    model[mapping(513)] = tuple([s1, s2, s3, s4, s5])
    total_model = total_model | s1 | s2 | s3 | s4 | s5

    s1 = {"B763", "B767-300ER", "B753", "B757-300ER"}
    s2 = {"B752", "B762", "A321", "A300", "B738", "B739", "B737-MAX8", "B737-MAX9", "B737-MAX10", "ARJ21"}
    s3 = {"B733", "B734", "B736", "B737", "B737-MAX7", "A320", "A319", "E190", "C919"}
    model[mapping(514)] = tuple([s1, s2, s3])
    total_model = total_model | s1 | s2 | s3

    s1 = {"B763", "B767-300ER", "B753", "B757-300ER"}
    s2 = {"B752", "B762", "A321", "A300", "B738", "B739", "B737-MAX8", "B737-MAX9", "B737-MAX10", "ARJ21"}
    s3 = {"B733", "B734", "B736", "B737", "B737-MAX7", "A320", "A319", "E190"}
    model[mapping(515)] = tuple([s1, s2, s3])
    total_model = total_model | s1 | s2 | s3

    s1 = {"B744", "B772", "B777-200LR", "B789", "A343", "A359"}
    s2 = {
        "A342",
        "A333",
        "A332",
        "B788",
        "B752",
        "B762",
        "B763",
        "A300",
        "B734",
        "B738",
        "B739",
        "B737-MAX8",
        "B737-MAX9",
        "B737-MAX10",
        "E190",
    }
    s3 = {"A321", "A320", "A319", "A310", "B732", "B733", "B735", "B736", "B737", "B737-MAX7", "C919"}
    model[mapping(3)] = tuple([s1, s2, s3])
    total_model = total_model | s1 | s2 | s3

    s1 = {
        "B734",
        "B738",
        "B739",
        "B737-MAX8",
        "B737-MAX9",
        "B737-MAX10",
        "B752",
        "B762",
        "B767-200ER",
        "B763",
        "B767-300ER",
        "A300",
        "A321",
    }
    s2 = {"B732", "B733", "B735", "B736", "B737", "B737-MAX7", "A310", "A319", "A320", "C919"}
    model[mapping(8)] = tuple([s1, s2])
    model[mapping(9)] = tuple([s1, s2])
    total_model = total_model | s1 | s2

    s1 = {"B744", "B788", "B789", "B747SP", "A332", "A333", "B772", "B777-200LR", "A359"}
    s2 = {"A300", "A312", "B752", "B753", "B762", "B763", "MD11"}
    s3 = {
        "A321",
        "A320",
        "A319",
        "B733",
        "B734",
        "B735",
        "B736",
        "B737",
        "B738",
        "B739",
        "B737-MAX7",
        "B737-MAX8",
        "B737-MAX9",
        "B737-MAX10",
        "MD90",
        "E190",
        "C919",
        "ARJ21",
    }
    model[mapping(17)] = tuple([s1, s2, s3])
    model[mapping(18)] = tuple([s1, s2, s3])
    total_model = total_model | s1 | s2 | s3

    s1 = {"B763", "B767-300ER", "B753", "B757-300ER", "MD11", "MD90"}
    s2 = {"B752", "B762", "A310", "A300"}
    s3 = {
        "B733",
        "B734",
        "B735",
        "B736",
        "B737",
        "B738",
        "B739",
        "B737-MAX7",
        "B737-MAX8",
        "B737-MAX9",
        "B737-MAX10",
        "A321",
        "A320",
        "A319",
        "E190",
        "C919",
        "ARJ21",
    }
    model[mapping(19)] = tuple([s1, s2, s3])
    model[mapping(20)] = tuple([s1, s2, s3])
    total_model = total_model | s1 | s2 | s3

    return model, total_model


# def get_model():
#
#     model = np.zeros(60)
#
#     s1 = {"A321", "B737-400", "B737-800", "B737-900", "B737-MAX8", "B737-MAX9", "B737-MAX10", "ARJ21"}
#     s2 = {"A319", "A320", "B737-300", "B737-500", "B737-600", "B737-700", "B737-MAX7", "EMB190", "C919"}
#     model[mapping(1)] = tuple([s1, s2])
#     model[mapping(305)] = tuple([s1, s2])
#     model[mapping(306)] = tuple([s1, s2])
#
#     s1 = {"A321", "B737-400", "B737-800", "B737-900", "B737-MAX8", "B737-MAX9", "B737-MAX10"}
#     s2 = {"A319", "A320", "B737-300", "B737-500", "B737-600", "B737-700", "B737-MAX7", "EMB190", "C919"}
#     model[mapping(2)] = tuple([s1, s2])
#     model[mapping(5)] = tuple([s1, s2])
#     model[mapping(6)] = tuple([s1, s2])
#     model[mapping(313)] = tuple([s1, s2])
#     model[mapping(314)] = tuple([s1, s2])
#     model[mapping(315)] = tuple([s1, s2])
#     model[mapping(317)] = tuple([s1, s2])
#     model[mapping(318)] = tuple([s1, s2])
#     model[mapping(320)] = tuple([s1, s2])
#     model[mapping(321)] = tuple([s1, s2])
#
#     s1 = {"A321", "B737-400", "B737-800", "B737-900", "B737-MAX8", "B737-MAX9", "ARJ21"}
#     s2 = {"B737-200", "B737-300", "B737-500", "B737-600", "B737-700", "B737-MAX7", "A318", "A319", "A320",
#           "EMB190", "C919"}
#     model[mapping(4)] = tuple([s1, s2])
#     model[mapping(7)] = tuple([s1, s2])
#
#     s1 = {"A321", "B737-400", "B737-800", "B737-900", "B737-MAX8", "B737-MAX9", "B737-MAX10", "ARJ21"}
#     s2 = {"B737-200", "B737-300", "B737-500", "B737-600", "B737-700", "B737-MAX7", "A319", "A320",
#           "EMB190", "C919"}
#     model[mapping(10)] = tuple([s1, s2])
#     model[mapping(11)] = tuple([s1, s2])
#     model[mapping(12)] = tuple([s1, s2])
#     model[mapping(13)] = tuple([s1, s2])
#     model[mapping(15)] = tuple([s1, s2])
#     model[mapping(16)] = tuple([s1, s2])
#
#     s1 = {"A321", "B737-400", "B737-800", "B737-900", "B737-MAX8", "B737-MAX9", "B737-MAX10", "ARJ21"}
#     s2 = {"B737-200", "B737-300", "B737-500", "B737-600", "B737-700", "B737-MAX7", "A319", "A320",
#           "EMB190"}
#     model[mapping(14)] = tuple([s1, s2])
#
#     s1 = {"B737-800", "B737-900", "B737-MAX8", "B737-MAX9", "B737-MAX10", "A321", "ARJ21"}
#     s2 = {"B737-200", "B737-300", "B737-400", "B737-500", "B737-600", "B737-700", "B737-MAX7", "A319", "A320",
#           "EMB190", "C919"}
#     model[mapping(21)] = tuple([s1, s2])
#     model[mapping(22)] = tuple([s1, s2])
#     model[mapping(23)] = tuple([s1, s2])
#     model[mapping(24)] = tuple([s1, s2])
#     model[mapping(25)] = tuple([s1, s2])
#     model[mapping(26)] = tuple([s1, s2])
#
#     s1 = {"A321", "B737-400", "B737-800", "B737-900", "B737-MAX8", "B737-MAX9", "B737-MAX10", "ARJ21"}
#     s2 = {"A319", "A320", "B737-300", "B737-500", "B737-600", "B737-700", "B737-MAX7", "C919"}
#     model[mapping(307)] = tuple([s1, s2])
#
#     s1 = {"A321", "B737-400", "B737-800", "B737-900", "B737-MAX8", "B737-MAX9", "B737-MAX10"}
#     s2 = {"A319", "A320", "B737-300", "B737-500", "B737-600", "B737-700", "B737-MAX7", "C919"}
#     model[mapping(316)] = tuple([s1, s2])
#
#     s1 = {"B757-300", "B767-300", "B767-300ER"}
#     s2 = {"B737-400", "B737-800", "B737-900", "B737-MAX8", "B737-MAX9", "B737-MAX10", "A321", "B757-200", "B767-200",
#           "A300", "ARJ21"}
#     s3 = {"B737-300", "B737-600", "B737-700", "B737-MAX7", "A319", "A320", "EMB190", "C919"}
#     model[mapping(308)] = tuple([s1, s2, s3])
#     model[mapping(312)] = tuple([s1, s2, s3])
#
#     s1 = {"A340-600", "B777-300", "B777-300ER", "A350-1000"}
#     s2 = {"B767-300", "B767-300ER", "B757-300", "A340-500", "B747-400", "B787-9", "A350-900"}
#     s3 = {"B777-200", "A340-200", "A330-300"}
#     s4 = {"B757-200", "B767-200", "B737-400", "B737-800", "B737-900", "B737-MAX8", "B737-MAX9", "B737-MAX10", "A312",
#           "A300", "B747SP"}
#     s5 = {"B737-300", "B737-600", "B737-700", "A319", "A320", "A310", "EMB190", "C919"}
#     model[mapping(309)] = tuple([s1, s2, s3, s4, s5])
#
#     s1 = {"A340-600", "B777-300", "B777-300ER", "A350-1000"}
#     s2 = {"B747-400", "A350-900"}
#     s3 = {"B767-300", "B767-300ER", "B757-300", "A340-500"}
#     s4 = {"B777-200", "A340-200", "A330-300", "A330-200"}
#     s5 = {"B757-200", "B767-200", "B737-400", "B737-800", "B737-900", "B737-MAX8", "B737-MAX9", "B737-MAX10", "A321",
#           "A300", "B747SP"}
#     s6 = {"B737-300", "B737-600", "B737-700", "B737-MAX7", "A319", "A320", "A310", "EMB190", "C919"}
#     model[mapping(310)] = tuple([s1, s2, s3, s4, s5, s6])
#
#     s1 = {"A340-600", "B777-300", "B777-300ER", "A350-1000"}
#     s2 = {"B787-9", "A350-900"}
#     s3 = {"B767-300", "B767-300ER", "B757-300", "A340-300", "A340-500", "B747-400", "B787-8"}
#     s4 = {"B777-200", "A340-200", "A330-300", "A330-200"}
#     s5 = {"B757-200", "B767-200", "B737-400", "B737-800", "B737-900", "B737-MAX8", "B737-MAX9", "B737-MAX10", "A321",
#           "A300", "B747SP"}
#     s6 = {"B737-300", "B737-600", "B737-700", "B737-MAX7", "A319", "A320", "A310", "EMB190", "C919"}
#     model[mapping(311)] = tuple([s1, s2, s3, s4, s5, s6])
#
#     s1 = {"A340-600", "B777-300", "B777-300ER", "A350-1000"}
#     s2 = {"B787-9", "A350-900"}
#     s3 = {"B767-300", "B767-300ER", "B757-300", "A340-300", "A340-500", "B747-400"}
#     s4 = {"B777-200", "A340-200", "A330-300", "A330-200"}
#     s5 = {"B757-200", "B767-200", "B737-400", "B737-800", "B737-900", "B737-MAX8", "B737-MAX9", "B737-MAX10", "A321",
#           "A300", "B747SP"}
#     s6 = {"B737-300", "B737-600", "B737-700", "B737-MAX7", "A319", "A320", "A310", "EMB190", "C919"}
#     model[mapping(319)] = tuple([s1, s2, s3, s4, s5, s6])
#
#     s1 = {"B737-800", "B737-900", "B737-MAX8", "B737-MAX9", "B737-MAX10", "A321", "ARJ21"}
#     s2 = {"B737-300", "B737-400", "B737-500", "B737-600", "B737-700", "B737-MAX7", "A320", "A319",
#           "EMB190", "C919"}
#     model[mapping(326)] = tuple([s1, s2])
#     model[mapping(327)] = tuple([s1, s2])
#     model[mapping(328)] = tuple([s1, s2])
#     model[mapping(329)] = tuple([s1, s2])
#     model[mapping(330)] = tuple([s1, s2])
#     model[mapping(331)] = tuple([s1, s2])
#     model[mapping(332)] = tuple([s1, s2])
#     model[mapping(516)] = tuple([s1, s2])
#     model[mapping(517)] = tuple([s1, s2])
#     model[mapping(518)] = tuple([s1, s2])
#     model[mapping(519)] = tuple([s1, s2])
#
#     s1 = {"A340-600", "B777-300", "B777-300ER"}
#     s2 = {"B747-400", "A340-500", "B787-9", "A350-900"}
#     s3 = {"A330-300", "A340-200", "B777-200", "B767-300", "B767-300ER", "B757-300", "B757-300ER", "B787-8"}
#     s4 = {"A321", "B737-800", "B737-900", "B737-MAX8", "B737-MAX9", "B737-MAX10", "B757-200", "B767-200", "A300",
#           "A330-200", "ARJ21"}
#     s5 = {"B737-300", "B737-400", "B737-600", "B737-700", "B737-MAX7", "A320", "B747SP", "EMB190", "C919"}
#     model[mapping(510)] = tuple([s1, s2, s3, s4, s5])
#     model[mapping(511)] = tuple([s1, s2, s3, s4, s5])
#     model[mapping(512)] = tuple([s1, s2, s3, s4, s5])
#     model[mapping(513)] = tuple([s1, s2, s3, s4, s5])
#
#     s1 = {"B767-300", "B767-300ER", "B757-300", "B757-300ER"}
#     s2 = {"B757-200", "B767-200", "A321", "A300", "B737-800", "B737-900", "B737-MAX8", "B737-MAX9", "B737-MAX10",
#           "ARJ21"}
#     s3 = {"B737-300", "B737-400", "B737-600", "B737-700", "B737-MAX7", "A320", "A319", "EMB190", "C919"}
#     model[mapping(514)] = tuple([s1, s2, s3])
#
#     s1 = {"B767-300", "B767-300ER", "B757-300", "B757-300ER"}
#     s2 = {"B757-200", "B767-200", "A321", "A300", "B737-800", "B737-900", "B737-MAX8", "B737-MAX9", "B737-MAX10",
#           "ARJ21"}
#     s3 = {"B737-300", "B737-400", "B737-600", "B737-700", "B737-MAX7", "A320", "A319", "EMB190"}
#     model[mapping(515)] = tuple([s1, s2, s3])
#
#     s1 = {"B747-400", "B777-200", "B777-200LR", "B787-9", "A340-300", "A350-900"}
#     s2 = {"A340-200", "A330-300", "A330-200", "B787-8", "B757-200", "B767-200", "B767-300", "A300",
#           "B737-400", "B737-800", "B737-900", "B737-MAX8", "B737-MAX9", "B737-MAX10", "EMB190"}
#     s3 = {"A321", "A320", "A319", "A310", "B737-200", "B737-300", "B737-500", "B737-600", "B737-700", "B737-MAX7",
#           "C919"}
#     model[mapping(3)] = tuple([s1, s2, s3])
#
#     s1 = {"B737-400", "B737-800", "B737-900", "B737-MAX8", "B737-MAX9", "B737-MAX10", "B757-200", "B767-200",
#           "B767-200ER", "B767-300", "B767-300ER", "A300", "A321"}
#     s2 = {"B737-200", "B737-300", "B737-500", "B737-600", "B737-700", "B737-MAX7", "A310", "A319",
#           "A320", "C919"}
#     model[mapping(8)] = tuple([s1, s2])
#     model[mapping(9)] = tuple([s1, s2])
#
#     s1 = {"B747-400", "B747-400", "B787-8", "B787-9", "B747SP", "A330-200", "A330-300", "B777-200",
#           "B777-200LR", "A350-900"}
#     s2 = {"A300", "A310-200", "B757-200", "B757-300", "B767-200", "B767-300", "MD11"}
#     s3 = {"A321", "A320", "A319", "B737-300", "B737-400", "B737-500", "B737-600", "B737-700", "B737-800", "B737-900",
#           "B737-MAX7", "B737-MAX8", "B737-MAX9", "B737-MAX10", "MD90", "EMB190", "C919", "ARJ21"}
#     model[mapping(17)] = tuple([s1, s2, s3])
#     model[mapping(18)] = tuple([s1, s2, s3])
#
#     s1 = {"B767-300", "B767-300ER", "B757-300", "B757-300ER", "MD11", "MD90"}
#     s2 = {"B757-200", "B767-200", "A310", "A300"}
#     s3 = {"B737-300", "B737-400", "B737-500", "B737-600", "B737-700", "B737-800", "B737-900",
#           "B737-MAX7", "B737-MAX8", "B737-MAX9", "B737-MAX10", "A321", "A320", "A319", "EMB190", "C919", "ARJ21"}
#     model[mapping(19)] = tuple([s1, s2, s3])
#     model[mapping(20)] = tuple([s1, s2, s3])
#
#     return model
